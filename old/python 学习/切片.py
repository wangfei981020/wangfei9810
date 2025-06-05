def trim(s):
    print(s)
    start = 0
    print('111111',len(s))
    while start < len(s) and s[start] == ' ':
        start += 1
    end = len(s)
    while end > start and s[end - 1] == ' ':
        end -= 1
    return s[start:end]


t1='hello  '

# 测试:
if trim(t1) != 'hello':
    print('测试失败!1')
elif trim('  hello') != 'hello':
    print('测试失败!!2')
elif trim('  hello  ') != 'hello':
    print('测试失败!3')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!4')
elif trim('') != '':
    print('测试失败!5')
elif trim('    ') != '':
    print('测试失败!6')
else:
    print('测试成功!')

