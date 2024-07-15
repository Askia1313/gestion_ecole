var swiper = new Swiper(".home-slider", {
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  loop: true,
  grabCursor: true,
});

var swiper = new Swiper(".home-courses-slider", {
  loop: true,
  grabCursor: true,
  spaceBetween: 20,
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    991: {
      slidesPerView: 3,
    },
  },
});

var swiper = new Swiper(".teachers-slider", {
  loop: true,
  grabCursor: true,
  spaceBetween: 20,
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    991: {
      slidesPerView: 3,
    },
  },
});

var swiper = new Swiper(".reviews-slider", {
  loop: true,
  grabCursor: true,
  spaceBetween: 20,
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    991: {
      slidesPerView: 3,
    },
  },
});

var swiper = new Swiper(".logo-slider", {
  loop: true,
  grabCursor: true,
  spaceBetween: 20,
  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    450: {
      slidesPerView: 2,
    },
    768: {
      slidesPerView: 3,
    },
    991: {
      slidesPerView: 4,
    },
    1200: {
      slidesPerView: 5,
    },
  },
});

let accordion = document.querySelectorAll('.faq .accordion-container .accordion');

accordion.forEach(acco => {
  acco.onclick = () => {
    accordion.forEach(dion => dion.classList.remove('active'));
    acco.classList.toggle('active');
  };
});

document.querySelector('.load-more .btn').onclick = () => {
  document.querySelectorAll('.courses .box-container .hide').forEach(show => {
    show.style.display = 'block';
  });
  document.querySelector('.load-more .btn').style.display = 'none';
};



  // Sélectionnez le menu-toggle et la barre de navigation
  const menuToggle = document.getElementById('menu-toggle');
  const navbar = document.getElementById('navbar');

  // Ajoutez un gestionnaire d'événement au clic sur le menu-toggle
  menuToggle.addEventListener('click', function() {
  // Basculez la visibilité de la barre de navigation
  navbar.classList.toggle('navbar-open');
  menuToggle.classList.toggle('menu-open');
});
