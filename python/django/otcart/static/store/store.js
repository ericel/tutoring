$('.grid').masonry({
    // set itemSelector so .grid-sizer is not used in layout
    itemSelector: '.card',
    // use element for option
    columnWidth: '.grid-sizer',
    percentPosition: true
})