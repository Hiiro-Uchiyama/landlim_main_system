$(document).ready(function(){
    
    (function($) {
        "use strict";

    
    jQuery.validator.addMethod('answercheck', function (value, element) {
        return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    // validate contactForm form
    $(function() {
        $('#contactForm').validate({
            rules: {
                name: {
                    required: true,
                    minlength: 2
                },
                subject: {
                    required: true,
                    minlength: 4
                },
                number: {
                    required: true,
                    minlength: 5
                },
                email: {
                    required: true,
                    email: true
                },
                message: {
                    required: true,
                    minlength: 20
                }
            },
            messages: {
                name: {
                    required: "お名前の入力はお済みですか?",
                    minlength: "お名前は2文字以上でなければなりません。"
                },
                subject: {
                    required: "件名の入力はお済みですか?",
                    minlength: "件名は4文字以上でなければなりません。"
                },
                number: {
                    required: "",
                    minlength: ""
                },
                email: {
                    required: "メールアドレスの入力はお済みですか?"
                },
                message: {
                    required: "このフォームを送信するにはお問い合わせ内容を書かなければなりません。",
                    minlength: "お問い合わせ内容20文字以上でなければなりません。"
                }
            },
        })
    })
        
 })(jQuery)
})