const app = new Vue({
    el: '#app',

    data: {
        collectionId: window.location.href.split('/').pop(),
        nextPage: 1,
        headers: [],
        rows: []
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
                    this.headers.forEach(header => {
                        rowValues.push(row[header])
                    })
                    this.rows.push(rowValues);
                })
            }, response => {

            });
        },
    }

});
