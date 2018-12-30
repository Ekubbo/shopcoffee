Vue.component('modal', {
	template: '#modal-template',
});

var app = new Vue({
	delimiters: ["[[","]]"],
	el: '#app',
	data: {
		selectedProduct: undefined,
		products: [],
		next_page: '/api/products/',
		showModal: false
	},
	mounted: function () {
		this.loadProducts();
	},
	methods: {
		loadProducts: function(event){
			if (this.next_page === null) {
				return;
			}

			var that = this;
			axios.get(this.next_page).then(function(response){
				that.products = that.products.concat(response.data['results']);
				that.next_page = response.data['next'];
			})
		},
		displayProduct: function (product) {
			this.selectedProduct = product;
			this.showModal = true;
		},
	}
});