MESSAGES = {
    'ar': {
        # عام
        'success':              'تمت العملية بنجاح',
        'error':                'حدث خطأ',
        'not_found':            'العنصر غير موجود',
        'unauthorized':         'غير مصرح لك بهذا الإجراء',
        'login_required':       'يجب تسجيل الدخول أولاً',
        'invalid_data':         'بيانات غير صحيحة',
        'server_error':         'خطأ في الخادم',

        # Auth
        'register_success':     'تم إنشاء الحساب بنجاح',
        'login_success':        'تم تسجيل الدخول بنجاح',
        'profile_updated':      'تم تحديث الملف الشخصي بنجاح',

        # Scanner
        'scan_success':         'تم فحص الورقة النقدية بنجاح',
        'scan_genuine':         'الورقة النقدية أصلية ✅',
        'scan_counterfeit':     'تحذير! الورقة النقدية مزيفة ❌',
        'scan_limit_reached':   'وصلت للحد اليومي من الفحوصات',
        'scan_history':         'تم جلب سجل الفحوصات بنجاح',

        # Policies
        'policy_fetched':       'تم جلب السياسة بنجاح',
        'app_policy_fetched':   'تم جلب سياسة التطبيق بنجاح',
        'policy_not_found':     'السياسة غير موجودة',
    },

    'en': {
        # General
        'success':              'Operation completed successfully',
        'error':                'An error occurred',
        'not_found':            'Item not found',
        'unauthorized':         'You are not authorized',
        'login_required':       'Authentication required',
        'invalid_data':         'Invalid data provided',
        'server_error':         'Internal server error',

        # Auth
        'register_success':     'Account created successfully',
        'login_success':        'Logged in successfully',
        'profile_updated':      'Profile updated successfully',

        # Scanner
        'scan_success':         'Banknote scanned successfully',
        'scan_genuine':         'Banknote is genuine ✅',
        'scan_counterfeit':     'Warning! Counterfeit banknote detected ❌',
        'scan_limit_reached':   'Daily scan limit reached',
        'scan_history':         'Scan history retrieved successfully',

        # Policies
        'policy_fetched':       'Policy retrieved successfully',
        'app_policy_fetched':   'App policy retrieved successfully',
        'policy_not_found':     'Policy not found',
    }
}


def get_message(key, lang='en'):
    """جلب الرسالة حسب اللغة"""
    language = lang if lang in MESSAGES else 'en'
    return MESSAGES[language].get(key, MESSAGES['en'].get(key, key))