var productPrices = {};

$(document).ready(function () {

    // Load products
    $.get(productListApiUrl)
        .done(function (response) {

            console.log("Products:", response);

            productPrices = {};

            var options = '<option value="">--Select--</option>';

            $.each(response, function (index, product) {

                options += '<option value="' + product.product_id + '">' +
                    product.name +
                    '</option>';

                productPrices[product.product_id] = product.price_per_unit;
            });

            $(".product-box select").html(options);
        })
        .fail(function (xhr) {
            console.log(xhr);
            alert("Cannot connect to backend");
        });


    // Add More Button
    $("#addMoreButton").click(function () {

        var row = $(".product-box").html();

        $("#itemsInOrder").append(row);

        calculateValue();
    });


    // Remove Row
    $(document).on("click", ".remove-row", function () {
        $(this).closest(".product-item").remove();
        calculateValue();
    });


    // Product Change
    $(document).on("change", ".cart-product", function () {

        var product_id = $(this).val();
        var price = productPrices[product_id] || 0;

        $(this)
            .closest(".product-item")
            .find(".product-price")
            .val(price);

        calculateValue();

    });


    // Quantity Change
    $(document).on("keyup change", ".product-qty", function () {
        calculateValue();
    });


    // Save Order
    $("#saveOrder").click(function () {

        var formData = $("form").serializeArray();

        var requestPayload = {
            customer_name: "",
            grand_total: 0,
            order_details: []
        };

        for (var i = 0; i < formData.length; i++) {

            var element = formData[i];

            switch (element.name) {

                case "customerName":
                    requestPayload.customer_name = element.value;
                    break;

                case "product_grand_total":
                    requestPayload.grand_total = element.value;
                    break;

                case "product":

                    if (element.value !== "") {

                        requestPayload.order_details.push({
                            product_id: element.value,
                            quantity: 0,
                            total_price: 0
                        });

                    }

                    break;

                case "qty":

                    if (requestPayload.order_details.length > 0) {

                        requestPayload.order_details[
                            requestPayload.order_details.length - 1
                        ].quantity = element.value;

                    }

                    break;

                case "item_total":

                    if (requestPayload.order_details.length > 0) {

                        requestPayload.order_details[
                            requestPayload.order_details.length - 1
                        ].total_price = element.value;

                    }

                    break;
            }
        }

        $.ajax({

            url: orderSaveApiUrl,

            type: "POST",

            data: {
                data: JSON.stringify(requestPayload)
            },

            success: function (response) {
                alert("Order Saved Successfully");
                console.log(response);
                location.reload();
            },

            error: function (xhr) {
                console.log(xhr.responseText);
                alert("Error while saving order");
            }

        });

    });

});