const app = new Vue({
    el: '#app',

    data: {
        collectionId: window.location.href.split('/').pop(),
        page: 1,
        headers: [],
        rows: []
    },

    mounted: function () {
        this.loadMore();
    },

    methods: {
        loadMore: function () {
            this.$http.get(`/api/collection-data/${this.collectionId}`).then(response => {
                this.headers = response.body.headers;
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
