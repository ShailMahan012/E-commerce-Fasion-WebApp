paypal.Buttons({
  // Order is created on the server and the order id is returned
  createOrder() {
    return fetch("/create-paypal-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: localStorage.getItem("products"),
    })
      .then((response) => response.json())
      .then((order) => order.id);
  },
  // Finalize the transaction on the server after payer approval
  onApprove(data) {
    return fetch("/capture-paypal-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        orderID: data.orderID,
        products: JSON.parse(localStorage.getItem("products"))
      })
    })
      .then((response) => response.json())
      .then((orderData) => {
        var form = gen_order_form()
        if (form != -1) {
          send_data(form, CHECKOUT_URL).then(result => {
            console.log(result)
            const element = document.getElementById('paypal-button-container');
            element.innerHTML = '<h3>Thank you for your payment!</h3>';
          })
        }
        // Successful capture! For dev/demo purposes:
        console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
        const transaction = orderData.purchase_units[0].payments.captures[0];
        alert(`Transaction ${transaction.status}: ${transaction.id}\n\nSee console for all available details`);
        // When ready to go live, remove the alert and show a success message within this page. For example:
        // Or go to another URL:  window.location.href = 'thank_you.html';
      });
  }
}).render('#paypal-button-container');
