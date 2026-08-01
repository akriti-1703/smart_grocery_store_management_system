var productPrices = {};

$(function () {
    //Json data by api call for order table
    $.get(productListApiUrl, function (response) {
        productPrices = {}
        if(response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, product) {
                options += '<option value="'+ product.product_id +'">'+ product.name +'</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            $(".product-box").find("select").empty().html(options);
        }
    });
});

$("#addMoreButton").click(function () {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    $(".product-box-extra .remove-row").last().removeClass('hideit');
    $(".product-box-extra .product-price").last().val('0.0');
    $(".product-box-extra .product-qty").last().val('1');
    $(".product-box-extra .product-total").last().val('0.0');
});

$(document).on("click", ".remove-row", function (){
    $(this).closest('.row').remove();
    calculateValue();
});

$(document).on("change", ".cart-product", function (){
    var product_id = $(this).val();
    var price = productPrices[product_id];

    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

$("#saveOrder").on("click", function () {

    var formData = $("form").serializeArray();

    var requestPayload = {
        customer_name: "",
        grand_total: 0,
        order_details: []
    };


    for (var i = 0; i < formData.length; i++) {

        var element = formData[i];

        switch(element.name) {

            case "customerName":
                requestPayload.customer_name = element.value;
                break;


            case "product_grand_total":
                requestPayload.grand_total = element.value;
                break;


            case "product":

                if(element.value != "") {

                    requestPayload.order_details.push({
                        product_id: element.value,
                        quantity: 0,
                        total_price: 0
                    });

                }

                break;


            case "qty":

                if(requestPayload.order_details.length > 0){

                    requestPayload.order_details[
                        requestPayload.order_details.length - 1
                    ].quantity = element.value;

                }

                break;


            case "item_total":

                if(requestPayload.order_details.length > 0){

                    requestPayload.order_details[
                        requestPayload.order_details.length - 1
                    ].total_price = element.value;

                }

                break;
        }
    }


    alert(JSON.stringify(requestPayload, null, 2));


    $.ajax({

        url: orderSaveApiUrl,

        type: "POST",

        data: {
            data: JSON.stringify(requestPayload)
        },


        success:function(response){

            alert("Order Saved Successfully");

            console.log(response);

        },


        error:function(xhr){

            console.log(xhr.responseText);

            alert("Error while saving order");

        }

    });


});