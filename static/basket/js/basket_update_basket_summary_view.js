// Delete item
$('.delete-button').on('click', function(e) {
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
    error: (err) => {
      console.log(err)
    }
  })
})

// Update item
$('.update-qty').on('change', function(e) {
  e.preventDefault();
  const productID = $(this).data('id');

  $.ajax({
    type: 'POST',
    url: basketUpdateURL,
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      productID: productID,
      productQty: $(`#update${productID}`).val(),
      action: 'update'
    },
    success: (json) => {
      // $('#update-qty').html(json.basket_qty);
      $(`#total-price${productID}`).html(json.item_total_price);

      $('#basket-qty').html(json.basket_qty);
      $('#basket-price').html(json.basket_price);
      $('#total').html(json.basket_price);
    },
    error: (err) => {
      console.log(err)
    }
  })
})