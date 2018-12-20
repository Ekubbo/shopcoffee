var app = new Vue({
	delimiters: ["[[","]]"],
	el: '#app',
	data: {
		products: [],
		next_page: '/api/products/',
	},
	mounted: function () {
		this.loadProducts();
	},
	methods: {
		loadProducts: function(event){
			if (this.next_page === null) {
				return
			}
			
			var that = this
			axios.get(this.next_page).then(function(response){
				that.products = that.products.concat(response.data['results']);
				that.next_page = response.data['next'];
			})
		},
	}
})