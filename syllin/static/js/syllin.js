/**
 * Created by Austin Scott on 2/26/2017.
 */

jQuery(window).load(function () {
    var $rowHeight = $('.grid-sizer').width();
    $('.grid-item').offsetHeight($rowHeight);
    $('.grid-item--width-2').offheight($rowHeight * 2);
});

