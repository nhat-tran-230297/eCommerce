const stripe = Stripe('pk_test_51IbAuCAycxBnrM9riSEfXpJShUDtkNpTz85izPEVoWlmQusYZEzei2YBnAna2JcbG0AYEIo8y3ohDnHbbYJvnHTL00qXcH7P5q')

const clientSecret = $('#submit').data('secret');

const elements = stripe.elements();

// acard style (JSX)
const style = {
    base: {
        color: '#000',
        lineHeight: '2.4',
        fontSize: '16px',
    }
};

const card = elements.create('card', { style: style });
card.mount('#card-element');

// display stripe error when 'onchange'
card.on('change', function (event) {
    var displayError = $('#card-errors')
    if (event.error) {
        displayError.text(event.error.message);
        displayError.addClass('alert alert-info');
    } else {
        displayError.text('');
        displayError.removeClass('alert alert-info');
    }
});

// payment
const paymentInfo =
{
    payment_method: {
        card: card,
        billing_details: {
            address: {
                line1: $('#custAdd').val(),
                line2: $('#custAdd2').val(),
            },
            name: $('custName').val()
        }
    }
}


// submit form
$('#payment-form').on('submit', function (event) {
    event.preventDefault();

    $.ajax({
        type: 'POST',
        url: orderAddURL,
        data: {
            order_key: clientSecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: 'post',
        },
        success: (json) => {
            console.log(json.status);
            stripe.confirmCardPayment(clientSecret, paymentInfo)
            .then((result) => {
                if (result.error) {
                    console.log('payment error')
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed')
                        // There's a risk of the customer closing the window before callback
                        // execution. Set up a webhook or plugin to listen for the
                        // payment_intent.succeeded event that handles any business critical
                        // post-payment actions.
                        window.location.replace(paymentCompleteURL);
                    }
                }
            })
        },

        error: (xhr, errmsg, error) => {
            console.log(error)
        }

    })




})
