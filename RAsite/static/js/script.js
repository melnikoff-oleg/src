$('#btn_1').click(function() {
  $('#modal_1').arcticmodal()
});

$(document).ready(function() {
	$(".select").selectBox();
});

$('.tabs_links li').click(function() {
  $('.tabs_links li').removeClass('active');
  $(this).addClass('active');
  $('.tabs_items .item').removeClass('active')
    .eq($(this).index()).addClass('active');
  $('.tabs_items_name .item').removeClass('active')
    .eq($(this).index()).addClass('active');
  return false;
});

$('.review .review_form .block_1 .link a').click(function() {
  $(this).hide();
  $('.review .review_form .block_1 form .save').removeClass('hide');
});


$('.review .review_block .left .block_1 .link').click(function() {
  $(this).hide();
  $(this).next().next().removeClass('hide');
});

$('.review .review_block .right .block_1 .link').click(function() {
  $(this).hide();
  $(this).next().next().removeClass('hide');
});

$('.review .review_block_2 .link').click(function() {
  $(this).hide();
  $(this).parent().next().next().addClass('redact');
  $(this).next().removeClass('hide');
});

$('.review .review_block .left .block_1 .link').click(function() {
  $(this).hide();
  $(this).prev().addClass('redact');
  $(this).next().next().removeClass('hide');
});

$('.review .review_block .right .block_1 .link').click(function() {
  $(this).hide();
  $(this).prev().addClass('redact');
  $(this).next().next().removeClass('hide');
});
