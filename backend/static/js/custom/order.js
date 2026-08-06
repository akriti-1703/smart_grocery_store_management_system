var productPrices = {};

$(document).ready(function () {

    // Load Products
    $.ajax({
        url: productListApiUrl,
        type: "GET",
        success: function (response) {

            console.log("Products:", response);

            var options = '<option value="">--Select Product--</option>';

            productPrices = {};

            $.each(response, function (index, product) {

                options +=
                    '<option value="' + product.product_id + '">' +
                    product.name +
                    '</option>';

                productPrices[product.product_id] = product.price_per_unit;
            });

            $(".product-box .cart-product").html(options);

            // Add first row automatically
            $("#addMoreButton").click();
        },
        error: function (xhr) {
            console.log(xhr);
            alert("Cannot load products");
        }
    });


    // Add More
    $("#addMoreButton").click(function () {

        var row = $(".product-box .product-item").clone();

        row.find(".cart-product")
            .html($(".product-box .cart-product").html())
            .val("");

        row.find(".product-price").val("0.0");
        row.find(".product-qty").val("1");
        row.find(".product-total").val("0.0");

        $("#itemsInOrder").append(row);
    });


    // Product Change
    $(document).on("change", ".cart-product", function () {

        var productId = $(this).val();

        var price = productPrices[productId] || 0;

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


    // Remove Row
    $(document).on("click", ".remove-row", function () {
        $(this).closest(".product-item").remove();
        calculateValue();
    });


    // Save Order
    $("#saveOrder").click(function () {

        var requestPayload = {
            customer_name: $("#customerName").val(),
            grand_total: $("#product_grand_total").val(),
            order_details: []
        };

        $(".product-item").each(function () {

            var product = $(this).find(".cart-product").val();

            if (product != "") {

                requestPayload.order_details.push({
                    product_id: product,
                    quantity: $(this).find(".product-qty").val(),
                    total_price: $(this).find(".product-total").val()
                });

            }

        });

        console.log(requestPayload);

        $.ajax({
            url: orderSaveApiUrl,
            type: "POST",
            data: {
                data: JSON.stringify(requestPayload)
            },
            success: function (response) {
                alert("Order Saved Successfully");
                location.reload();
            },
            error: function (xhr) {
                console.log(xhr.responseText);
                alert("Error while saving order");
            }
        });

    });

});
