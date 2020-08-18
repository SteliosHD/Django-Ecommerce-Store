// get all the buttons 
var updateBtns = document.getElementsByClassName('update-cart')

// loop through all the buttons
// needs the script above the body in the main.html
for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){

        // get the data
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, "action: ", action)

        // if user is authenticated or not
        console.log("USER: ", user)
        if(user === 'AnonymousUser'){
                addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}


function addCookieItem(productId, action){
    console.log('Not logged in')

    if(action == 'add'){
        if(cart[productId] === undefined){
            cart[productId] = {'quantity' : 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
            cart[productId]['quantity'] -= 1

            if (cart[productId]['quantity']<=0){
                console.log('Remove Item')
                delete cart[productId]
            }
    }
console.log('Cart: ', cart)
document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
location.reload()
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    var url = '/update_item/'

    // this is a function (promise) that makes a request syntax: fetch().then().then() 
    // fetch always succeeds if it gets a response from the server. only if not it will raise an error. e.g 404 fetch succeeds
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })
    .then((response) =>{ //arrow function the same as function(){}
        return response.json() // parse the response as a JSON
    })
    .then((data) =>{
        console.log('data:', data)  //use nested then to get the data from the api
        location.reload()
    })
}