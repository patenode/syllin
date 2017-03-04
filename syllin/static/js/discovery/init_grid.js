/**
 * Created by Austin Scott on 3/3/17.
 *
 * This file initializes the libraries Masonry and imagesLoaded, which are being used to deliver the
 * album art in an infinite-scrolling irregular grid. Masonry sizes and stacks elements into the grid
 * while imagesLoaded allows for elements to hold their proper size on the page as each of their content loads.
 */
var $grid = $('.grid').masonry({
    // Set itemSelector, .grid-sizer is not used in actual layout
    itemSelector: '.grid-item',

    // This element is solely used for getting the width of the grid
    columnWidth: '.grid-sizer',

    // Use percentage-based CSS positioning
    percentPosition: true
});

// Layout Masonry again as each image loads
$grid.imagesLoaded().progress(function () {
    $grid.masonry('layout');
});