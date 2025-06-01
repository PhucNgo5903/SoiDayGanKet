$(document).ready(function() {
    // Khởi tạo DataTable
    $('#mytable').DataTable();
    
    // Toggle sidebar - Gộp cả vanilla JS và jQuery
    $('#btn-sidebar').click(function() {
        console.log("Sidebar toggle clicked");
        $('.sidebar').toggleClass('active');
        
        // Đóng tất cả submenu khi đóng sidebar
        if (!$('.sidebar').hasClass('active')) {
            $('.submenu').removeClass('open');
        }
    });
    
    // Toggle submenu chỉ khi sidebar đang mở
    $('.submenu > a').click(function(e) {
        e.preventDefault();
        
        // Chỉ cho phép mở submenu khi sidebar active
        if ($('.sidebar').hasClass('active')) {
            const $submenu = $(this).parent();
            
            // Đóng các submenu khác
            $('.submenu').not($submenu).removeClass('open');
            
            // Toggle submenu hiện tại
            $submenu.toggleClass('open');
        } else {
            // Nếu sidebar chưa mở, mở sidebar trước
            $('.sidebar').addClass('active');
            
            // Sau khi mở sidebar, mở submenu
            setTimeout(() => {
                $(this).parent().addClass('open');
            }, 300); // Đợi animation sidebar hoàn thành
        }
    });
    
    // Đóng submenu khi click outside sidebar
    $(document).click(function(e) {
        if (!$(e.target).closest('.sidebar').length) {
            $('.submenu').removeClass('open');
        }
    });
    
    // Ngăn việc đóng submenu khi click vào submenu items
    $('.submenu ul').click(function(e) {
        e.stopPropagation();
    });
    
    // Thêm hiệu ứng hover vào sidebar items
    $('.sidebar ul li a').hover(
        function() {
            if (!$('.sidebar').hasClass('active')) {
                $(this).attr('title', $(this).find('.links_name').text());
            }
        },
        function() {
            $(this).removeAttr('title');
        }
    );
});