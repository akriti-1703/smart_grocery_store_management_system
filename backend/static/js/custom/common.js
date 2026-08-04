// Define your api here
// Backend URL
var BASE_URL = "https://smart-grocery-store-management-system-4.onrender.com";

// API URLs
var productListApiUrl = BASE_URL + "/getProducts";
var uomListApiUrl = BASE_URL + "/getUOM";
var productSaveApiUrl = BASE_URL + "/insertProduct";
var productDeleteApiUrl = BASE_URL + "/deleteProduct";
var orderListApiUrl = BASE_URL + "/getAllOrders";
var orderSaveApiUrl = BASE_URL + "/insertOrder";
var productsApiUrl = 'https://fakestoreapi.com/products';
function callApi(method, url, data) {
    $.ajax({
        method: method,
        url: url,
        data: data,
        success: function(response){
            console.log(response);
            location.reload();
        },
        error: function(err){
            console.log(err);
            alert("API Error");
        }
    });
}
function calculateValue() {
    var total = 0;

    $(".product-item").each(function () {

        var qty = parseFloat($(this).find(".product-qty").val()) || 0;
        var price = parseFloat($(this).find(".product-price").val()) || 0;

        var itemTotal = qty * price;

        $(this).find(".product-total").val(itemTotal.toFixed(2));

        total += itemTotal;
    });

    $("#product_grand_total").val(total.toFixed(2));
}

function orderParser(order) {
    return {
        id : order.id,
        date : order.employee_name,
        orderNo : order.employee_name,
        customerName : order.employee_name,
        cost : parseInt(order.employee_salary)
    }
}

function productParser(product) {
    return {
        id : product.id,
        name : product.employee_name,
        unit : product.employee_name,
        price : product.employee_name
    }
}

function productDropParser(product) {
    return {
        id : product.id,
        name : product.title
    }
}

//To enable bootstrap tooltip globally
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// });