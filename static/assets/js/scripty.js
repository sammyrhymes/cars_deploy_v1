 // Carousel scrolling functionality
 const carousel = document.getElementById('carousel');
 const scrollLeftButton = document.getElementById('scrollLeft');
 const scrollRightButton = document.getElementById('scrollRight');
 
 let currentIndex = 0;
   const imagesToShow = 4;  // Number of images to show at once
   const totalImages = {{ images|length }};
   
 scrollRightButton.addEventListener('click', () => {
     if (currentIndex < totalImages - imagesToShow) {
         currentIndex += imagesToShow; // Scroll to the next 4 images
         carousel.style.transform = `translateX(-${currentIndex * 25}%)`; // 25% because each image is 1/4 width
     }
 });
 
 scrollLeftButton.addEventListener('click', () => {
     if (currentIndex > 0) {
         currentIndex -= imagesToShow;
         carousel.style.transform = `translateX(-${currentIndex * 25}%)`;
     }
 });