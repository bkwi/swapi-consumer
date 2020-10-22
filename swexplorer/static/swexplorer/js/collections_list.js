const app = new Vue({
    el: '#app',

    data: {
        collections: [],
        processing: false
    },

    methods: {
        fetchCollections: function () {
            if (this.processing) return;

            this.processing = true
            this.$http.post('/api/fetch-collections', {}, reqOptions).then(response => {
                this.processing = false;
            }, response => {
                this.processing = false;
                alert(`Something went wrong! ${response.body.error}`);
            });
        },
    }

});
