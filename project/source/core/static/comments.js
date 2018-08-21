$(document).ready(
    function () {
        autoload = function () {
            $('.autoload').each(function () {
                $(this).load($(this).data('url'));
            });
        };

        autoload();
        window.setInterval(autoload, 2000);

        $(document).on('submit','.addlike', function () {
            var form = this;
            $.post(
                $(form).attr('action'),
                $(form).serialize(),
                function (response) {
                    autoload();
                }
            );
            return false;
        });

        $(document).on('click', '.commentadd', function () {
             $('.add_comment_form')
                 .load($(this).data('url'))
                 .attr('action', $(this).data('url'));
            return true;
        });


        $(document).on('submit', '.add_comment_form', function () {
            var form = this;
            $.post(
                $(form).attr('action'),
                $(form).serialize(),
                function (response) {
                    autoload();
                }
            );
            $('#exampleModal').modal('toggle');
            return false;
        });

        $('.selectmultiple').each( function () {
            $(this).attr('class', 'chosen-select');
        });

        $('.chosen-select').chosen();

    }
);

