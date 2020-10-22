const app = new Vue({
    el: '#app',

    data: {
        collections: [],
        processing: false
    },

    mounted: function () {
        this.$http.get('/api/collections').then(response => {
            this.collections = response.body.collections;
        });
    },

    methods: {
        fetchCollections: function () {
            if (this.processing) return;

            this.processing = true
            this.$http.post('/api/collections', {}, reqOptions).then(response => {
                this.processing = false;
                this.collections.unshift(response.body);
            }, response => {
                this.processing = false;
                alert(`Something went wrong! ${response.body.error}`);
            });
        },
    }

});
