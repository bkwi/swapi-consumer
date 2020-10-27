const app = new Vue({
    el: '#app',

    data: {
        collectionId: window.location.href.split('/').pop(),
        nextPage: 1,
        headers: [],
        rows: [],
        selectedHeaders: [],
        valueCount: []
    },

    computed: {
        orderedSelectedHeaders: function () {
            // sort selected headers so they are in the same order as in csv,
            // visually better + easier to cache search results in api
            let items = [...this.selectedHeaders];
            items.sort((a, b) => this.headers.indexOf(a) - this.headers.indexOf(b));
            return items
        },

        valueCountHeaders: function () {
            return this.orderedSelectedHeaders.concat('count');
        },
    },

    mounted: function () {
        this.loadMore();
    },

    methods: {
        loadMore: function () {
            let url = `/api/collection-data/${this.collectionId}/page/${this.nextPage}`;
            this.$http.get(url).then(response => {
                this.headers = response.body.headers;
                this.nextPage = response.body.next_page;
                response.body.rows.forEach(row => {
                    let rowValues = [];
                    this.headers.forEach(header => rowValues.push(row[header]));
                    this.rows.push(rowValues);
                });
            }, response => {

            });
        },

        headerClicked: function (header) {
            if (this.selectedHeaders.indexOf(header) >= 0) {
               this.selectedHeaders.splice(this.selectedHeaders.indexOf(header), 1);
            } else {
                this.selectedHeaders.push(header);
            };

            // do nothing when there are no headers selected
            if (this.selectedHeaders.length === 0) return;

            let options = {
                params: {
                    values: this.orderedSelectedHeaders
                }
            };
            this.$http.get(`/api/collection-data/${this.collectionId}/value-count`, options).then(response => {
                this.valueCount = response.body.value_count;
            });
        },
    }

});
