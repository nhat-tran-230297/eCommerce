$(document).on('click', '#add-button', function (e) {
  e.preventDefault();

  $.ajax({
    type: 'POST',
    url: basketAddURL,
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      productID: $('#add-button').val(),
      productQty: $('#select').val(),
      action: 'post'
    },
    success: (json) => {
      console.log(json.basket_qty)
      document.getElementById('basket-qty').innerHTML = json.basket_qty;
    },
    error: (xhr, errMessage, err) => {

    }
  })
})