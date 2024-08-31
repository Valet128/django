$(document).ready(function () {

    //BURGER
    $('.header__burger').click(function (event) {
        $('.header__burger, .header__menu').toggleClass('active');
        $('body').toggleClass('lock');
    });
    
    //MODAL
    $('.btn__link_exit').click(function (event) {
        $('.modal-wrap').toggleClass('active');
    });
    $('.btn__link_cancel').click(function (event) {
        $('.modal-wrap').toggleClass('active');
    });

    //SWIPER
    new Swiper('.image-slider', {
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true    
        },
        slidesPerView: 2,
        spaceBetween: 30,
        autoplay: {
            delay: 5000,
            stopOnLastSlide: false,
            disableOnInteraction: false
        },
        speed: 1000,
        loop: true,
        breakpoints: {
            0: {
            slidesPerView: 1,
            },
            767: {
            slidesPerView: 2,   
            }
        }
    });
    new Swiper('.image-feedback', {
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true
        },
        slidesPerView: 5,
        spaceBetween: 30,
        autoplay: {
            delay: 10000,
            stopOnLastSlide: false,
            disableOnInteraction: false
        },
        speed: 1000,
        loop: true,
        breakpoints: {
            0: {
                slidesPerView: 1,
            },
            500: {
                slidesPerView: 3,
            },
            767: {
                slidesPerView: 5,
            }
        }
    });
    //MORE
    $('#product-more').click(function (event) {
        
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "/home/indexelem");
        xhr.onload = () => {
            if (xhr.status == 200) {
                
                const products = JSON.parse(xhr.responseText);
                var children = document.getElementById("row").children.length;
                if (children < products.length) {
                    var allLength = products.length - children;
                    var adderLength = 0;
                    if (allLength > 3)
                    {
                        adderLength = 3;
                    }
                    else
                    {
                        adderLength = allLength;
                    }
                    const row = document.getElementById("row");
                    var htmlText = ``;
                    for (var i = children; i < children + adderLength; i++) {
                        if (products[i].category == "Прошедшие(Запись)")
                        { 
                            htmlText += `<div class="product__column">
                    <div class="product__item">
                        <div class="product__img">
                            <img src="${products[i].image}"/>
                        </div>
                        <div class="product__title">
                            <p>${products[i].name}</p>
                        </div>
                        <div class="product__price">
                            <p>${products[i].price} ₽</p>
                        </div>
                        <div class="product__date">
                            <p></p>      
                        </div>
                        <div class="product-btn"> 
                            <div class="product-btn__row"> 
                                <div class="product-btn__column"> 
                                    <a class="btn__link" href="home/product/${products[i].id}">Подробнее...</a>
                                </div>
                                <div class="product-btn__column">
                                    <a class="btn__link" href="home/buyproduct/${products[i].id}">Купить</a>
                                </div>
                            </div>
                        </div>
                    </div>
                        </div>`;
                    }
                            else
                    {
                        htmlText += `<div class="product__column">
                    <div class="product__item">
                        <div class="product__img">
                            <img src="${products[i].image}"/>
                        </div>
                        <div class="product__title">
                            <p>${products[i].name}</p>
                        </div>
                        <div class="product__price">
                            <p>${products[i].price} ₽</p>
                        </div>
                        <div class="product__date">
                            <p>${products[i].dateAndTime}</p>      
                        </div>
                        <div class="product-btn"> 
                            <div class="product-btn__row"> 
                                <div class="product-btn__column"> 
                                    <a class="btn__link" href="home/product/${products[i].id}">Подробнее...</a>
                                </div>
                                <div class="product-btn__column">
                                    <a class="btn__link" href="home/buyproduct/${products[i].id}">Купить</a>
                                </div>
                            </div>
                        </div>
                    </div>
                        </div>`;
                    }
                   


                    }
                    row.innerHTML += htmlText;
                } else {
                    document.getElementById('product-more').innerText = "А все..."
                }
            }
            else { console.log("Server response: ", xhr.statusText); }

        }
        xhr.send();
    });
   
    if ($('#select-content').val() == "Новый")
    {
        const div = $('.select-input');
        const newInput = document.createElement('input');
        newInput.setAttribute('type', 'text');
        $('.form-item__text').addClass(".input-select")
        newInput.setAttribute('id', 'input-select');
        newInput.setAttribute('class', 'form-item__text');
        div.append(newInput);
    }

    $('#select-content').change(function () {
        if ($('#select-content').val() == "Новый" && $('#input-select').length == false) {
            const div = $('.select-input');
            const newInput = document.createElement('input');
            newInput.setAttribute('type', 'text');
            newInput.setAttribute('id', 'input-select');
            newInput.setAttribute('class', 'form-item__text');
            div.append(newInput);
        }
        else if ($('#select-content').val() == "Новый") {
            $('#input-select').show();
        }
        else {
            $('#input-select').hide();
        }
    });
    $('#input-select').keyup(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
           var valueInput = $('#input-select').val();
            document.getElementById('select-content').innerHTML += `<option selected>${valueInput}</option>`;
            $('#input-select').val('');
            $('#input-select').hide();
            
        }
    });

   
    $('#input-select').blur(function (event) {
            event.preventDefault();
        var valueInput = $('#input-select').val();
        document.getElementById('select-content').innerHTML += `<option selected>${valueInput}</option>`;
        $('#input-select').val('');
        $('#input-select').hide();
        
    });

    //content-profile
    if ($('.pack__list').has('.pack-list__column') == false)
    {
        $(this).parent().find('.table__column').innerHTML = ''; 
    }
   
    $('.pack__title').click(function (event) {
        $(this).siblings().toggleClass('active');
    });
    $('.pack-list__title').click(function (event) {
        $(this).siblings().toggleClass('active');
    });

    //progress

    
    

});
