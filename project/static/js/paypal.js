paypal.Buttons({
  // Order is created on the server and the order id is returned
  createOrder() {
    var form = gen_order_form()
    if (form != -1) {
    return send_data(form, '/create-paypal-order')
      .then((order) => order.id);
    }
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
            localStorage.setItem("products", '[]') // Empty cart after checkout
            const invoice_id = orderData.purchase_units[0].payments.captures[0].invoice_id
            const element = document.getElementById('form');
            element.innerHTML = `<div class="row"><h1 class="title">Thanks for your order</h1></div><div class="row"><h3>INVOICE: ${invoice_id}</h3></div>`
            hide_paypal()

        // Successful capture! For dev/demo purposes:
        console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
        msg("Transaction Completed", "primary")
        // const transaction = orderData.purchase_units[0].payments.captures[0];
        // alert(`Transaction ${transaction.status}: ${transaction.id}\n\nSee console for all available details`);
        // When ready to go live, remove the alert and show a success message within this page. For example:
        // Or go to another URL:  window.location.href = 'thank_you.html';
      });
  }
}).render('#paypal-button');
