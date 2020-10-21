const app = new Vue({
    el: '#app',

    data: {
        collections: []
    },

    methods: {
        fetchCollections: function () {
            this.$http.post('/api/fetch-collections', {}, reqOptions).then(response => {
                console.log("fetch response", response);
            }, response => {
                alert(`Something went wrong! Response status: ${response.status}`);
            });
        },
    }

});
