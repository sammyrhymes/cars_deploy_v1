const carousels = document.querySelectorAll('.carousel');

carousels.forEach((carousel, index) => {
  const windowWidth = window.innerWidth;
  const isSmallScreen = windowWidth < 768; // Adjust this value for your desired breakpoint

  let intervalId;
  let currentIndex = 0;

  const updateCarousel = () => {
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
  };

  const previousSlide = () => {
    console.log('prev')
    currentIndex--;
    if (currentIndex < 0) {
      currentIndex = carousel.children.length - 1;
    }
    updateCarousel();
  };

  const nextSlide = () => {
    console.log('next')

    currentIndex++;
    if (currentIndex >= carousel.children.length) {
      currentIndex = 0;
    }
    updateCarousel();
  };



  // Add event listeners to buttons
  const prevButton = carousel.parentElement.querySelector('.prev');
  const nextButton = carousel.parentElement.querySelector('.next');

  prevButton.addEventListener('click', previousSlide);
  nextButton.addEventListener('click', nextSlide);

});