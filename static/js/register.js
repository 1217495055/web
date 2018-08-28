$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;

	// 当用户名框失去焦点时判断用户名
	$('#user_name').blur(function() {
		check_user_name();
	});

	// 当密码框失去焦点时的判断
	$('#pwd').blur(function() {
		check_pwd();
	});

	// 当确认密码框失去焦点时的判断
	$('#cpwd').blur(function() {
		check_cpwd();
	});

	// 当邮箱框失去焦点时的判断
	$('#email').blur(function() {
		check_email();
	});

	// 勾选（是否同意协议）框失去焦点时的判断
	$('#allow').click(function() {
		// 如果已经勾选，则隐藏提示
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		// 否则，提示勾选（同意该协议）
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});

	// 判断用户名
	function check_user_name(){
		// 获取输入的用户名的长度
		var len = $('#user_name').val().length;
		// 判断长度是否在（５～２０），如果不在，则提示请输入5-20个字符的用户名
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名')
			$('#user_name').next().show();
			error_name = true;
		}
		// 否则判断该用户是否存在
		else
		{
			// 判断用户名是否已经存在，直接发送一个Ajax请求
		    $.get('/user/register_exist/?uname='+$('#user_name').val(),function(data){
		        // 如果返回１，则表示用户名已经存在，则提示,用户名已经存在
		        if(data.count>=1){
		            $('#user_name').next().html('用户名已经存在');
		            $('#user_name').next().show();
		            error_name=true;
		        // 返回０，则表示用户名不存在，则继续以下操作
		        }else{
			        $('#user_name').next().hide();
			        error_name = false;
		        }
		    });
		}
	}

	// 判断密码
	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<6||len>20)
		{
			$('#pwd').next().html('密码最少6位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确')
			$('#email').next().show();
			error_check_password = true;
		}

	}

	// 点击注册按钮时会触发，如果全为空，则阻止表单提交
	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});
})