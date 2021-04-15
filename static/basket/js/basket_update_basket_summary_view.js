// Delete item
$(document).on('click', '.delete-button', function(e) {
  e.preventDefault();
  const productID = $(this).data('id');

  $.ajax({
    type: 'POST',
    url: basketDeleteURL,
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      productID: productID,
      action: 'delete'
    },
    success: (json) => {
      $(`#item${productID}`).remove();

      $('#basket-qty').html(json.basket_qty);
      $('#basket-price').html(json.basket_price);

      $('#total').html(json.basket_price);

    },
    error: (xhr, errMessage, err) => {
      console.log(err)
    }
  })
})

// Update item
$(document).on('click', '.update-button', function(e) {
  e.preventDefault();
  const productID = $(this).data('id');
  console.log(productID)

  $.ajax({
    type: 'POST',
    url: basketAddURL,
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      productID: productID,
      productQty: $(`#select${productID}`).val(),
      action: 'post'
    },
    success: (json) => {
      // $('#select-qty').html(json.basket_qty);
      $(`#total-price${productID}`).html(json.item_total_price);

      $('#basket-qty').html(json.basket_qty);
      $('#basket-price').html(json.basket_price);
      $('#total').html(json.basket_price);
    },
    error: (xhr, errMessage, err) => {
      console.log(err)
    }
  })
})