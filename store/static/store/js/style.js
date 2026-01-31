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

    $('#container').click(function(event) {
        if (event.target.id === 'product-more'){
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "/get_products");
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
                        let category = ''
                        let href = ''
                        let date = ''
                        let btn_value = ''
                        let options = {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: 'numeric',
                            minute: 'numeric',
                            second: 'numeric'
                            };
                        if (products[i].fields.category === 3){
                            category += 'Бесплатно'
                            href += `free_event/${products[i].pk}/`
                            btn_value += 'Записаться'
                        }
                        else {
                            category += products[i].fields.price + '₽'
                            href = `placing_an_order/${products[i].pk}/`
                            btn_value += 'Купить'
                        }
                        
                        if (products[i].fields.interaction.name === "Запись" || products[i].fields.date === null){
                            date = ''
                        }
                        else
                        {
                            date =  new Intl.DateTimeFormat('ru-RU', { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric'}).format(new Date(products[i].fields.date))
                        }
                        htmlText += `<div class="product__column">
                            <div class="product__item">
                                <div class="product__img">
                                    <img src="${MEDIA_URL}${products[i].fields.image}"/>
                                </div>
                                <div class="product__title">
                                    <p>${products[i].fields.name}</p>
                                </div>
                                <div class="product__price">
                                 <p>${category}</p>
                                </div>
                                <div class="product__date">
                                    <p>${date}</p>
                                </div>
                                <div class="product-btn"> 
                                    <div class="product-btn__row"> 
                                        <div class="product-btn__column"> 
                                            <a class="btn__link product-btn__link" href="product/${products[i].pk}/">Подробнее...</a>
                                        </div>
                                        <div class="product-btn__column"> 
                                            <a class="btn__link product-btn__link" href="${href}">${btn_value}</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>`;


                    }
                    row.innerHTML += htmlText;
                } else {
                    document.getElementById('product-more').innerText = "А все..."
                }
            }
            else { console.log("Server response: ", xhr.statusText); }

        }
        xhr.send();
    }
    else {console.log('NOTHINg')}
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
