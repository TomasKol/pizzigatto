// event listeners for meal type buttons (menu navbar)
let menuButtons = document.querySelectorAll('.menu-button');
for (let i = 0; i < menuButtons.length; i++) {
  let btn = menuButtons[i];
  btn.addEventListener('click', () => {
    const typeId = btn.getAttribute('data-id');
    $('.items-container').hide();
    $(`#items-container-type-${typeId}`).show().removeClass('bord-b');
    $('.menu-button').removeClass('menu-button-selected');
    btn.classList.add('menu-button-selected');
  });
}

// event listeners for add to cart buttons (non-pizzas)
let cartButtons = document.querySelectorAll('.add-to-cart-button');
for (let i = 0; i < cartButtons.length; i++) {
  let btn = cartButtons[i];
  btn.addEventListener('click', () => {
    const btnId = btn.getAttribute('data-id'); //get id of the item/form of the particular item
    const size = btn.getAttribute('data-size'); //get desired size of the menu item
    
    // extra cheese for sub -> corresponding forms end with "-cheese" and here we identify them thanks
    // to the data-cheese="-cheese" attribute. Yes, WITH the dash.
    // IMPORTANT: leave the dash at the beggining of "-cheese" and don't add it the the form id!
    let extraCheese = '';
    if (btn.getAttribute('data-cheese')) {
      extraCheese = btn.getAttribute('data-cheese');
    }
    //get data from the particular form
    //DO NOT ADD THE DASH!!!
    const data = $(`#form-item-${btnId}-${size}${extraCheese}`).serialize(); 
    
    $.ajax({
      url: $(`#form-item-${btnId}-${size}`).data('url'),
      type: 'POST',
      data: data,
    });
  });
}

// event listener for add to cart button (pizza)
let addToCartButton = document.querySelector('#pizza-form-submit');
if (addToCartButton) {

  addToCartButton.addEventListener('click', () => {
  
    // form and size of pizza are required
    if ( !$('input[name=form]:checked').val() || !$('input[name=size]:checked').val() ) {
      return alert('Make sure you have selected form and size of your pizza!');
    }

    $.ajax({
      url: $('#form-pizza').data('url'),
      method: 'POST',
      data: $('#form-pizza').serialize(),
      success: success
    });
  
    function success(response) {
      let notification = '';
      const cartUrl = addToCartButton.getAttribute('data-url');
      if (response.error) {
        notification = `<p>${response.error} <a href="${cartUrl}">your cart</a>.</p>` 
      } else {
        const name = response.message.charAt(0).toUpperCase() + response.message.slice(1);
        notification = `<p>${name} was added to <a href="${cartUrl}">your cart</a>.</p>` 
      }
      document.querySelector('#form-pizza').reset();
      $('#added-pizzas').prepend(notification);
    }
  });
}

// limit: max 4 toppings on a pizza
const toppingCheckboxes = document.querySelectorAll('.topping-checkbox');
for (let i = 0; i < toppingCheckboxes.length; i++) {
  const chbx = toppingCheckboxes[i];
  chbx.addEventListener('change', () => {
    const maxToppings = 4;
    const checkedToppings = document.querySelectorAll('.topping-checkbox:checked').length
    if (checkedToppings > maxToppings) {
      alert('Max 4 toppings on a pizza.')
      chbx.click();
    }
  });
}

// event listener for delete from cart buttons
let deleteButtons = document.querySelectorAll('.delete-from-cart-button');
for (let i = 0; i < deleteButtons.length; i++) {
  let btn = deleteButtons[i];
  btn.addEventListener('click', () => {
    // no need to delegate the event: new buttons are not created dynamically
    const itemId = btn.getAttribute('data-id');
    const data = $(`#form-delete-item-${itemId}`).serialize();

    $.ajax({
      url: $(`#form-delete-item-${itemId}`).data('url'),
      method: 'POST',
      data: data,
      success: success
    });

    function success(response) {
      $(`#cart-item-${response.deletedCartItemId}`).remove();
      updateCartTotal();
    }
  });
}

// event listeners for plus/minus cart item amount
const plusMinusButtons = document.querySelectorAll('.change-amount-button');
for (let i = 0; i < plusMinusButtons.length; i++) {
  const btn = plusMinusButtons[i];
  const itemId = btn.getAttribute('data-id');

  // enable/disable minus buttons at page load
  const amountAtLoad = $(`#cart-item-${itemId}`).data('amount_at_load');
  minusButtonEnabling(amountAtLoad, itemId);

  // listener
  btn.addEventListener('click', () => {
    const direction = btn.getAttribute('data-direction'); // plus or minus -> +1 | -1
    // let's not have an input with name "direction"; only add this value to the serialized data from the form
    const data = $(`#form-plus-amount-${itemId}`).serialize() + '&direction=' + direction;

    $.ajax({
      url: $(`#form-plus-amount-${itemId}`).data('url'),
      type: 'POST',
      data: data,
      success: success
    });
    
    function success(response) {
      
      // update the amount display
      const amountDom = $(`#cart-item-${itemId}`).find('.amount'); //target the child .amount
      amountDom.html(response.amount + 'x');

      // update the total price for this item*amount
      const totalPriceDom = $(`#cart-item-${itemId}`).find('.price-for-amount');
      totalPriceDom.html('$' + response.priceTotal);

      // if amount == 1: disable the minus button
      minusButtonEnabling(response.amount, itemId);

      // update total price for the cart
      updateCartTotal();
    }
  });
}

// event listeners for accept order buttons
const acceptOrderButtons = document.querySelectorAll('.accept-order-button');
for (let i = 0; i < acceptOrderButtons.length; i++) {
  let btn = acceptOrderButtons[i];
  btn.addEventListener('click', () => {
    const url = btn.getAttribute('data-url');
    const orderId = btn.getAttribute('data-id');
    const data = `id=${orderId}&${$('#get-token').serialize()}`;
    $.ajax({
      url: url,
      method: 'POST',
      data: data,
      success: success
    });

    function success(response) {
      $(`#accept-order-${orderId}-button-container`).html('<p>accepted</p>');
    }
  });
}

// event listeners for delete meal type buttons
const deleteMealTypeButtons = document.querySelectorAll('.delete-meal-type-button');
for (let i = 0; i < deleteMealTypeButtons.length; i++) {
  const btn = deleteMealTypeButtons[i];
  const type = btn.getAttribute('data-name');
  const typeId = btn.getAttribute('data-id');
  btn.addEventListener('click', () => {
    if (!confirm(`Sure want to delete ${type} and all its menu items? This cannot be undone.`)) {
      return
    }

    const data = `id=${typeId}&${$('#get-token').serialize()}`;

    $.ajax({
      url: btn.getAttribute('data-url'),
      method: 'POST',
      data: data, 
      success: success
    });

    function success(response) {
      if (response.success) {
        window.location.replace(btn.getAttribute('data-redirect'));
      } 
    }
  });
}

// event listener for delete menu item buttons
const deleteMenuItemButtons = document.querySelectorAll('.delete-menu-item-button');
for (let i = 0; i < deleteMenuItemButtons.length; i++) {
  const btn = deleteMenuItemButtons[i];
  const itemName = btn.getAttribute('data-name'); 
  btn.addEventListener('click', () => {
    if (!confirm(`Sure want to delete ${itemName}? This cannot be undone.`)) {
      return
    }
    
    const itemId = btn.getAttribute('data-id');
    const data = `id=${itemId}&${$('#get-token').serialize()}`;

    $.ajax({
      url: btn.getAttribute('data-url'),
      method: 'POST',
      data: data,
      success: success
    });

    function success(response) {
      if (response.success) {
        window.location.replace(btn.getAttribute('data-redirect'));
      }
    }
  });
}

// event listener for delete topping buttons
const deleteToppingButtons = document.querySelectorAll('.delete-topping-button');
for (let i = 0; i < deleteToppingButtons.length; i++) {
  const btn = deleteToppingButtons[i];
  btn.addEventListener('click', () => {
    const toppingName = btn.getAttribute('data-name'); 
    if (!confirm(`Sure want to delete ${toppingName} topping? This cannot be undone.`)) {
      return;
    }

    const toppingId = btn.getAttribute('data-id');
    const data = `id=${toppingId}&${$('#get-token').serialize()}`;

    $.ajax({
      url: btn.getAttribute('data-url'),
      method: 'POST',
      data: data,
      success: success
    });

    function success(response) {
      if (response.success) {
        window.location.replace(btn.getAttribute('data-redirect'));
      } 
    }
  });
}

// HELPERS

// disable the minus button if current amount is 1
function minusButtonEnabling(amount, itemId) {
  if (amount == '1') {
    $(`#minus-${itemId}-button`).prop('disabled', true);
  } else {
    $(`#minus-${itemId}-button`).prop('disabled', false);
  }
}

function updateCartTotal() {
  const itemTotals = document.querySelectorAll(".price-for-amount");
  let cartTotal = 0.0;

  if (itemTotals.length > 0) {
    for (let i = 0; i < itemTotals.length; i++) {
      const el = itemTotals[i];
      cartTotal += parseFloat((el.innerHTML).replace('$', ''));
    }
    $("#cart-total-price").html('$' + cartTotal.toFixed(2));
  
  // if empty cart
  } else {
    $("#cart-total-label").html('Your cart is emtpy.');
    $("#cart-total-price").remove();
    $('#place-order-form').remove();

  }
}

// feather icons stroke color for add to cart button
const svgs = document.querySelectorAll('svg');
for (let i = 0; i < svgs.length; i++) {
  if (svgs[i].parentElement.classList.contains('add-to-cart-button')) {
    svgs[i].setAttribute('stroke', 'rgb(23, 162, 184)');
  }
}
