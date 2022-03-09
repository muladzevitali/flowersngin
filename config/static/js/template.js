jQuery(document).ready(function ($) {
	var mobilewidth = 1024; //mobile delimeter
	var headerMenuHeight = $('#header-menu').outerHeight();
	let menuOffset = $('#header-menu').offset().top;
	let showcaseHeight = $('.js-showcase').outerHeight();

	//fixed-menu
	$(window).on("scroll", function () {
		menuOnScroll();
		headerMenuHeight = $('#header-menu').outerHeight();
	})

	function menuOnScroll() {
		currOffset = $(this).scrollTop() - 1;
		if (currOffset >= menuOffset) {
			$('.wrapper').addClass("sticky-menu");
		}
	}

	function mobileMenu(selector) {

		let menu = $(selector);
		let button = menu.find('#hamburger');
		let overlay = menu.find('#menu-overlay');
		let link = menu.find('.main-menu a');

		button.on('click', () => toggleMenu());
		overlay.on('click', () => toggleMenu());
		link.on('click', () => toggleMenu());

		function toggleMenu() {
			if ($(window).width() <= mobilewidth) {
				menu.toggleClass('menu-active');

				if (menu.hasClass('menu-active')) {
					$('body').css('overflow', 'hidden');
				} else {
					$('body').css('overflow', 'visible');
					$('.submenu-child').hide();
					$('.submenu > a').removeClass('focus');
				}
			}
		}
	}

	//init menu
	mobileMenu('#header-menu');

	//smooth scroll
	$(".js-scroll-to").on("click", function (e) {
		if ($('.wrapper').hasClass('sticky-menu')) {
			$('.js-showcase').slideUp(500);
			showcaseHeight = 0;
		} else {
			$('.js-showcase').slideUp(500);
			$('.wrapper').addClass("sticky-menu");
		}
		let url = $(this).attr('href');
		let anchor = getHashFromUrl(url);
		let top = $('#' + anchor).offset().top - parseInt($('#' + anchor).css('marginTop')) - showcaseHeight;
		$('body,html').animate({
			scrollTop: top - headerMenuHeight
		}, 750);
	});

	$(window).scroll(function () {
		if ($('.wrapper').hasClass('sticky-menu')) {
			showcaseHeight = 0;
		} else {
			$('.js-showcase').slideUp(500);
			$('.wrapper').addClass("sticky-menu");
		}
	})

	if (window.location.hash) scroll(0, 0);
	// avoid some browsers issue
	setTimeout(function () {
		scroll(0, 0);
	}, 1);

	$(window).on('load', function () {
		let anchor = $(':target');
		if (anchor.length > 0) {
			$('.wrapper').addClass("sticky-menu");
			$('.js-showcase').slideUp(500);
			let top = $(anchor).offset().top - parseInt($(anchor).css('marginTop')) - showcaseHeight;
			$('body,html').animate({
				scrollTop: top + headerMenuHeight - 20
			}, 750);
		}
	});

	//scrollspy
	var topMenu = $(".home-page .main-menu"),
		menuItems = topMenu.find('a.js-scroll-to'),
		// Anchors corresponding to menu items
		scrollItems = menuItems.map(function () {
			var url = $(this).attr("href");
			var anchor = '#' + getHashFromUrl(url);
			try {
				var item = $(anchor);
				if (item.length) {
					return item;
				}
			} catch { }
		});

	// Bind to scroll
	$(window).scroll(function () {
		// Get container scroll position
		var fromTop = $(this).scrollTop() + headerMenuHeight + 70;

		// Get id of current scroll item
		var cur = scrollItems.map(function () {
			if ($(this).offset().top < fromTop)
				return this;
		});
		// Get the id of the current element
		cur = cur[cur.length - 1];
		var id = cur && cur.length ? cur[0].id : "";
		// Set/remove active class
		menuItems
			.parent().removeClass("active")
			.end().filter("[href='/#" + id + "']").parent().addClass("active");
	});

	function getHashFromUrl(url) {
		return $("<a />").attr("href", url)[0].hash.replace(/^#/, "");
	}

	//slider
	function initReviewsSlider() {
		$('.js-reviews-slider').slick({
			autoplay: true,
			slidesToShow: 5,
			slidesToScroll: 1,
			arrows: false,
			variableWidth: true,
			centerMode: true,
			centerPadding: 0,
			responsive: [
				{
					breakpoint: 1025,
					settings: {
						slidesToShow: 3
					}
				},
				{
					breakpoint: 600,
					settings: {
						slidesToShow: 2
					}
				},
				{
					breakpoint: 426,
					settings: {
						slidesToShow: 1,
						variableWidth: false,
					}
				}
			]
		});
	}
	initReviewsSlider();

	//tabs
	$('.js-tabs').each(function () {
		$(this).find('.js-tabs__head li').each(function (i) {
			$(this).click(function () {
				$(this).addClass('active').siblings().removeClass('active')
					.closest('.js-tabs').find('.js-tabs__content').hide().removeClass('active').eq(i).fadeIn().addClass('active');
			});
		});
	});

	//add row to botanicals tab layout	
	function wrapBotanicList(oddRow, evenRow) {
		$('.js-botanic-list > .row > .botanic-single').unwrap();
		if (oddRow > 0 && evenRow > 0) {
			$('.js-botanic-list').each(function (index, element) {
				// element == this
				let childDivs = ($('> .botanic-single', element).length);
				for (let index = 0; index < childDivs; index++) {
					$('> .botanic-single:lt(' + oddRow + ')', element).wrapAll('<div class="row --odd" />');
					$('> .botanic-single:lt(' + evenRow + ')', element).wrapAll('<div class="row --even" />');
				}
			});
		}
	}
	$(window).on("load resize", function () {
		let ww = $(window).width();
		if (ww >= 1500) wrapBotanicList(7, 8);
		else if (ww >= 1300 && ww < 1500) wrapBotanicList(6, 7);
		else if (ww >= 1100 && ww < 1300) wrapBotanicList(5, 6);
		else if (ww >= 900 && ww < 1100) wrapBotanicList(5, 4);
		else if (ww >= 600 && ww < 900) wrapBotanicList(4, 3);
		else if (ww < 600) wrapBotanicList(0, 0);
	})

	//number
	$('.js-like-number .like-number__p').click(function (e) {
		e.preventDefault;
		let curValue = $(this).prev('input').val();
		$(this).prev('input').val(++curValue)
	});
	$('.js-like-number .like-number__m').click(function (e) {
		e.preventDefault;
		let curValue = $(this).next('input').val(),
			minValue = $(this).data('minval');
		if (--curValue <= minValue) {
			$(this).next('input').val('0')
		} else {
			$(this).next('input').val(--curValue)
		}
	});

	//form options
	$('#client_type').on('change', function () {
		if ($(this).is(":checked")) {
			$('.js-company__field').show(200);
			$('.js-company__field input').prop('required', true);
		} else {
			$('.js-company__field').hide(200);
			$('.js-company__field input').val('').prop('required', false);
		}
	});
	//show/hide delivery address
	$('#delivery-address').on('change', function () {
		showHideDeliveryAddress();
	});
	//rules for pickup option
	$('#ophalen-in-winkel').on('change', function () {
		if ($(this).is(":checked")) {
			$('.js-hide__delivery').hide(200);
			$('.js-hide__delivery input').prop("checked", false);
			showHideDeliveryAddress();
		} else {
			$('.js-hide__delivery').show(200);
		}
	});

	function showHideDeliveryAddress() {
		if ($('#delivery-address').is(":checked")) {
			$('.js-delivery-address').show(200);
			$('.js-delivery-address .required input').prop('required', true);
		} else {
			$('.js-delivery-address').hide(200);
			$('.js-delivery-address .required input').val('').prop('required', false);
		}
	}

});
