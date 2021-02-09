
let stripe = Stripe('pk_test_51HvgcNC0y3iCJrXqhi04GCxf5kYhgPvHlcXuO2kaigKKurbsieGPc9GgdJ63XTLBmvAD9nIeyC1Qyml16AXHUouf00ogCGCDbc');


// Event handler
let checkoutBtn = document.querySelector("#subscription-checkout-button");

checkoutBtn.addEventListener('click', function () {
    stripe.redirectToCheckout({
        sessionId: sessionid
    }).then(function (result) {
    });
});