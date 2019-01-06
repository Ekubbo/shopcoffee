Vue.component('modal', {
	delimiters: ["[[","]]"],
	template: '#modal-template',
	props: ['product'],
	data: function () {
		return {
			quantity: 1
		}
	},
	watch: {
		quantity: function(newValue) {
			this.quantity = parseInt(this.quantity);
			if (this.quantity > 20) this.quantity = 20;
			if (this.quantity < 1) this.quantity = 1;
		}
	},
});

Vue.component('list-products', {
	delimiters: ["[[","]]"],
	template: '#list-products',
	data: function () {
		return {
			next_page: '/api/products/',
			products: [],
			is_show_detail: false,
			detail_product: undefined,
		}
	},
	mounted: function () {
		this.next_page = '/api/products/';
		this.loadProducts();
	},
	methods: {
		loadProducts: function(event){
			if (this.next_page === null) return;

			var that = this;
			axios.get(this.next_page).then(function(response){
				that.products = that.products.concat(response.data['results']);
				that.next_page = response.data['next'];
			})
		},
		displayDetail: function(product){
			this.detail_product = product;
			this.is_show_detail = true;
		},
	},
});

Vue.component('counter', {
	delimiters: ["[[","]]"],
	template: '<span>[[ animatedNumber ]]</span>',
	props: ['number'],
	data: function(){
		return {
			tweened_number: 0
		}
	},
	mounted: function () {
		this.tweened_number = this.number;
	},
	computed: {
		animatedNumber: function() {
			return this.tweened_number.toFixed(0);
		}
	},
	watch: {
		number: function(newValue) {
			TweenLite.to(this.$data, 0.5, { tweened_number: newValue });
		}
	}
});

Vue.component("cart-modal", {
	delimiters: ["[[","]]"],
	template: "#cart-modal-template",
	props: ['products'],
	data: function(){
		return {
			show: false,
		}
	},
	computed: {
		totalCost: function() {;
			let result = 0;
			for (var i = 0; i < this.products.length; i++) {
				result += this.products[i].price * this.products[i].quality;
			}
			return result;
		}
	},
	mounted: function () {
		this.show = true;
		this.total_cost = this.totalCost();
	},
});

var app = new Vue({
	delimiters: ["[[","]]"],
	el: '#app',
	data : {
		cart_list: [],
		is_show_cart: false,
		cout_products_in_cart: 0,
	},
	mounted: function () {
		this.updateCartList();
	},
	methods: {
		setToCart: function(item, quantity){
			var params = {quantity : quantity, slug : item.slug, }
			var config = {headers: {'X-CSRFToken': csrftoken}, }
			
			that = this;
			axios.put("/api/basket/add/", params, config).then(function(response){
				that.updateCartList();
			});
		},
		addToCart: function(item, quantity){
			var params = {quantity : quantity, slug : item.slug, }
			var config = {headers: {'X-CSRFToken': csrftoken}, }

			that = this;
			axios.post("/api/basket/add/", params, config).then(function(response){
				that.updateCartList();
			});
		},
		removeFromCart: function(product){
			var that = this;
			axios.post("/api/basket/delete/", {"slug": product.slug}).then(function(response){
				that.updateCartList();
			});
		},
		updateCartList: function(){
			var that = this;
			axios.get("/api/basket/list/").then(function(response){
				that.cart_list = response.data;
				cout_products_in_cart = 0;
				for (var i = that.cart_list.length - 1; i >= 0; i--) {
					cout_products_in_cart += that.cart_list[i].quality;
				}
				that.cout_products_in_cart = cout_products_in_cart;
			});
		},
	},
});