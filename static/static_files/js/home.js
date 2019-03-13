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

Vue.component('modal-order', {
	delimiters: ["[[","]]"],
	template: '#modal-order-template',
	props: ['cart_list'],
	data: function () {
		return {
			errors: {
			},
			fields:{
				first_name: '',
				last_name: '',
				phone_client: '',
				adress_client: '',
				comment: '',
			},
			confirm_checkout: false,
		}
	},
	methods:{
		confirmCheckout: function(){
			var params = this.fields;
			var config = {headers: {'X-CSRFToken': csrftoken}};

			var that = this;
			axios.post("/api/order/", params, config).then(function(response){
				that.confirm_checkout = true;
			}).catch(function(error){
				that.errors = error.response.data;
			});
		},
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
				result += this.products[i].product.price * this.products[i].quantity;
			}
			return result;
		}
	},
	mounted: function () {
		this.show = true;
	},
});

var app = new Vue({
	delimiters: ["[[","]]"],
	el: '#app',
	data : {
		cart_list: [],
		is_show_cart: false,
		is_show_order: false,
		cout_products_in_cart: 0,
	},
	mounted: function () {
		this.updateCartList();
	},
	methods: {
		addToCart: function(item, quantity){
			var params = {quantity : quantity, slug : item.slug};
			var config = {headers: {'X-CSRFToken': csrftoken}};

			that = this;
			axios.post("/api/cart/add/", params, config).then(function(response){
				that.updateCartList();
			});
		},
		removeFromCart: function(product){
			var params = {"slug": product.slug};
			var config = {headers: {'X-CSRFToken': csrftoken}};

			var that = this;
			axios.post("/api/cart/delete/", params, config).then(function(response){
				that.updateCartList();
			});
		},
		updateCartList: function(){
			var that = this;
			axios.get("/api/cart/list/").then(function(response){
				that.cart_list = response.data;

                cout_products_in_cart = 0;
				for (var i = that.cart_list.length - 1; i >= 0; i--) {
					cout_products_in_cart += that.cart_list[i].quantity;
				}
				that.cout_products_in_cart = cout_products_in_cart;
			});
		},
	},
});
