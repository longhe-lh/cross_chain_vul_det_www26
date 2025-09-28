import re
import json
from typing import Dict, List

from utils.util.util import read_file_by_row_encode


# Extract Key Ops

def extract_key_ops(json_path: str, chain_type: str) -> Dict[str, List[str]]:
    """
    解析 JSON，提取所有 KeyOp 不为空的函数及其 KeyOp 内容。
    json_path: blg文件路径
    chain_type: 包括src_chain, rel_chain, det_chain 三种类型
    返回格式: {函数名: [KeyOp1, KeyOp2, ...], ...}
    """
    with open(json_path, 'r', encoding='gbk') as f:
        data = json.load(f)

    blg = data.get('blg', {})
    if not blg:
        # print('[警告] JSON 中未找到 blg 字段')
        blg = data # 在测试的情况下
        # return {}
    # 取出跨链桥
    contract_blg = list(blg.values())[0]

    result = {}

    chain = contract_blg.get(chain_type, {})
    events = chain.get('events', {})
    result[chain_type] = {}
    result[chain_type]["events"] = {}
    for event_name, event_dict in events.items():
        result[chain_type]["events"][event_name] = {}

        def dfs(res, node):
            try:
                func_name = node.get('func_name')
            except Exception as e:
                func_name = node.get('even_name')
            file_name = node.get('file_name')
            key_ops = node.get('key_ops', [])

            if func_name and key_ops:
                res[func_name] = {"file_name": file_name, "key_ops": []}
                if func_name not in res:
                    pass
                res[func_name]["key_ops"].extend(key_ops)
            child = node.get('child', {})
            for child_node in child.values():
                dfs(res, child_node)

        for root_node in event_dict.values():
            dfs(result[chain_type]["events"][event_name], root_node)

    return result


# Python

def find_py_function_body(src_path, func_name):
    """
    只匹配有函数体的 def func_name(...)\n    排除声明/抽象
    """
    # with open(src_path, "r", encoding="gbk") as f:
    #     code = f.read()
    code = read_file_by_row_encode(src_path)
    code_no_comment = re.sub(r'#.*', '', code)
    pattern = re.compile(r'def\s+' + re.escape(func_name) + r'\s*\([^)]*\):', re.MULTILINE)
    matches = list(pattern.finditer(code_no_comment))
    for match in matches:
        lines = code_no_comment[match.end():].splitlines()
        func_lines = []
        indent = None
        for line in lines:
            if not line.strip():
                func_lines.append(line)
                continue
            leading = len(line) - len(line.lstrip())
            if indent is None:
                if leading == 0:
                    break
                indent = leading
            if leading < indent:
                break
            func_lines.append(line)
        return code_no_comment[match.start():match.end()] + '\n' + '\n'.join(func_lines)
    return None


def trace_dependencies_py(src_path, func_body, statement, visited_vars=None):
    """
    在Python文件中找到关键操作的依赖语句链
    """
    if visited_vars is None:
        visited_vars = set()
    dependencies = []
    # 过滤 for/while/if/elif 头部
    if re.match(r'^\s*(for|while|if|elif)\s*\(', statement):
        return dependencies
    # 提取变量和函数名
    tokens = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', statement))
    keywords = {'if', 'elif', 'else', 'return', 'for', 'while', 'break', 'continue', 'def', 'class', 'import', 'from',
                'as', 'with', 'try', 'except', 'finally', 'raise', 'assert', 'yield', 'lambda', 'global', 'nonlocal',
                'del', 'pass', 'True', 'False', 'None', 'not', 'and', 'or', 'in', 'is', 'print', 'input'}
    tokens = [t for t in tokens if t not in keywords]
    for token in tokens:
        if token in visited_vars:
            continue
        visited_vars.add(token)
        # 匹配赋值语句
        assign_pattern = re.compile(r'(^|\n)\s*' + re.escape(token) + r'\s*=([^=].*)\n')
        assign_found = False
        for m in assign_pattern.finditer(func_body + '\n'):
            line = m.group(0).lstrip('\n').rstrip('\n').strip()
            dependencies.append(line)
            right_expr = line.split('=', 1)[1].strip()
            dependencies += trace_dependencies_py(src_path, func_body, right_expr, visited_vars)
            assign_found = True
        if not assign_found:
            # 查找是否为函数调用
            call_pattern = re.compile(re.escape(token) + r'\s*\(')
            if call_pattern.search(func_body):
                sub_body = find_py_function_body(src_path, token)
                if sub_body:
                    dependencies.append(f'def {token}(...) ...')
    return dependencies


# Solidity

def find_sol_function_body(src_path, func_name):
    """
    只匹配有函数体的 function func_name(...) { ... }
    排除接口/抽象函数声明
    """
    # with open(src_path, "r", encoding="gbk") as f:
    #     code = f.read()
    code = read_file_by_row_encode(src_path)
    code_no_comment = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
    # 匹配所有 function func_name(...) ... { 的位置
    # pattern = re.compile(r'(function|modifier)\s+' + re.escape(func_name) + r'\s*\([^)]*\)[\s\S]*?{', re.MULTILINE)
    # 修复 bug , solidity 中的特殊函数，如 fallback 和 receive 函数
    matches = None
    if func_name == "fallback" or func_name == "receive":
        pattern = re.compile(r'(function|modifier)\s+' + re.escape(func_name) + r'\s*\([^)]*\)[\s\S]*?{', re.MULTILINE)
        temp_match = list(pattern.finditer(code_no_comment))
        if not temp_match:
            pattern = re.compile(r'(?:fallback|receive)\s*\([^)]*\)\s*(external)?[\s\S]*?{', re.MULTILINE)
            matches = list(pattern.finditer(code_no_comment))
        else:
            matches = temp_match
    else:
        pattern = re.compile(r'(function|modifier)\s+' + re.escape(func_name) + r'\s*\([^)]*\)[\s\S]*?{', re.MULTILINE)
        matches = list(pattern.finditer(code_no_comment))
    for match in matches:
        # 检查 function 声明和 { 之间是否有分号
        func_decl = code_no_comment[match.start():match.end()]
        if ';' in func_decl:
            continue  # 跳过声明
        # 找到函数体
        start = match.start()
        stack = 1
        i = match.end()
        while i < len(code_no_comment) and stack > 0:
            if code_no_comment[i] == '{':
                stack += 1
            elif code_no_comment[i] == '}':
                stack -= 1
            i += 1
        return code_no_comment[start:i]
    return None


def trace_dependencies_sol(src_path, func_body, statement, visited_vars=None):
    """
    在.sol文件中找到关键操作的依赖语句链
    """
    if visited_vars is None:
        visited_vars = set()
    dependencies = []
    # 过滤 for/while/if 头部
    if re.match(r'^\s*(for|while|if)\s*\(', statement):
        return dependencies # 跳过控制结构头部
    # 提取变量和函数名
    tokens = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', statement))
    keywords = {'require', 'if', 'else', 'return', 'for', 'while', 'true', 'false', 'address', 'uint', 'int',
                'string', 'bool', 'public', 'private', 'external', 'internal', 'memory', 'storage', 'view', 'pure',
                'payable', 'mapping', 'event', 'emit', 'function', 'contract', 'struct', 'enum', 'break',
                'continue', 'new', 'delete', 'this', 'super', 'msg', 'block', 'tx'}
    # 筛选变量名
    tokens = [t for t in tokens if t not in keywords]
    for token in tokens:
        if token in visited_vars:
            continue
        visited_vars.add(token)
        assign_pattern = re.compile(r'(^|;)	*([a-zA-Z0-9_\[\]]+\s+)?' + re.escape(token) + r'\s*=(?!=|=|>|<)(.*);')
        assign_found = False
        for m in assign_pattern.finditer(func_body):
            line = m.group(0).lstrip('; \n').strip()
            # 检查该赋值语句是否在 for/while/if 头部括号内
            for_head_pattern = re.compile(r'(for|while|if)\s*\(([^)]*)\)')
            skip = False
            for for_head in for_head_pattern.finditer(func_body):
                if line in for_head.group(2):
                    skip = True
                    break
            if skip:
                continue
            dependencies.append(line)
            right_expr = line.split('=', 1)[1].rstrip(';').strip()
            dependencies += trace_dependencies_sol(src_path, func_body, right_expr, visited_vars)
            assign_found = True
        if not assign_found:
            # 查找是否为函数调用
            call_pattern = re.compile(re.escape(token) + r'\s*\(')
            if call_pattern.search(func_body):
                sub_body = find_sol_function_body(src_path, token)
                if sub_body:
                    dependencies.append(f'function {token}(...) {{...}}')
    return dependencies


# Java

def find_java_function_body(src_path, func_name):
    """
    只匹配有函数体的 [修饰符] 返回类型 func_name(...) { ... }
    排除接口/抽象声明
    """
    # with open(src_path, "r", encoding="gbk") as f:
    #     code = f.read()
    code = read_file_by_row_encode(src_path)
    code_no_comment = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
    # 匹配所有 func_name(...) ... { 的位置
    pattern = re.compile(r'(public|private|protected|static|final|synchronized|abstract|native|transient|\s)*' +
                         r'[a-zA-Z0-9_<>\[\]]+\s+' + re.escape(func_name) + r'\s*\([^)]*\)[^{;]*{', re.MULTILINE)
    matches = list(pattern.finditer(code_no_comment))
    for match in matches:
        # 检查声明和 { 之间是否有分号
        func_decl = code_no_comment[match.start(): match.end()]
        if ";" in func_decl:
            continue # 跳过声明
        # 找到函数体
        start = match.start()
        stack = 1
        i = match.end()
        while i < len(code_no_comment) and stack > 0:
            if code_no_comment[i] == '{':
                stack += 1
            elif code_no_comment[i] == '}':
                stack -= 1
            i += 1
        return code_no_comment[start:i]
    return None


def trace_dependencies_java(src_path, func_body, statement, visited_vars=None):
    """
    在Java文件中找到关键操作的依赖语句链
    """
    if visited_vars is None:
        visited_vars = set()
    dependencies = []
    # 过滤 for/while/if/switch 头部
    if re.match(r'^\s*(for|while|if|switch)\s*\(', statement):
        return dependencies
    # 提取变量和函数名
    tokens = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', statement))
    keywords = {'if', 'else', 'return', 'for', 'while', 'switch', 'case', 'break', 'continue', 'public', 'private',
                'protected', 'static', 'final', 'synchronized', 'abstract', 'native', 'transient', 'volatile',
                'class', 'interface', 'enum', 'extends', 'implements', 'import', 'package', 'void', 'int', 'long',
                'float', 'double', 'char', 'byte', 'short', 'boolean', 'true', 'false', 'null', 'this', 'super',
                'new', 'try', 'catch', 'finally', 'throw', 'throws', 'instanceof', 'assert'}
    tokens = [t for t in tokens if t not in keywords]
    for token in tokens:
        if token in visited_vars:
            continue
        visited_vars.add(token)
        # 匹配赋值语句
        assign_pattern = re.compile(r'(^|;)\s*([a-zA-Z0-9_<>\[\]]+\s+)?' + re.escape(token) + r'\s*=([^=].*);')
        assign_found = False
        for m in assign_pattern.finditer(func_body):
            line = m.group(0).lstrip('; \n').strip()
            dependencies.append(line)
            right_expr = line.split('=', 1)[1].rstrip(';').strip()
            dependencies += trace_dependencies_java(src_path, func_body, right_expr, visited_vars)
            assign_found = True
        if not assign_found:
            # 查找是否为函数调用
            call_pattern = re.compile(re.escape(token) + r'\s*\(')
            if call_pattern.search(func_body):
                sub_body = find_java_function_body(src_path, token)
                if sub_body:
                    dependencies.append(f'function {token}(...) {{...}}')
    return dependencies


# Go

def find_go_function_body(src_path, func_name):
    """
    只匹配有函数体的 func func_name(...) { ... }
    排除接口/声明
    """
    # with open(src_path, "r", encoding="gbk") as f:
    #     code = f.read()
    code = read_file_by_row_encode(src_path)
    code_no_comment = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
    pattern = re.compile(r'func\s+(?:\([^)]+\)\s*)?' + re.escape(func_name) + r'\s*\([^)]*\)[^{]*{', re.MULTILINE)
    matches = list(pattern.finditer(code_no_comment))
    for match in matches:
        func_decl = code_no_comment[match.start():match.end()]
        if ";" in func_decl:
            continue
        start = match.start()
        stack = 1
        i = match.end()
        while i < len(code_no_comment) and stack > 0:
            if code_no_comment[i] == '{':
                stack += 1
            elif code_no_comment[i] == '}':
                stack -= 1
            i += 1
        return code_no_comment[start:i]
    return None


def trace_dependencies_go(src_path, func_body, statement, visited_vars=None):
    """
    在Go文件中找到关键操作的依赖语句链
    """
    if visited_vars is None:
        visited_vars = set()
    dependencies = []
    if re.match(r'^\s*(for|if|switch)\s*\(', statement):
        return dependencies
    tokens = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', statement))
    keywords = {'if', 'else', 'return', 'for', 'switch', 'case', 'break', 'continue', 'func', 'var', 'const', 'type',
                'struct', 'interface', 'map', 'chan', 'go', 'defer', 'range', 'select', 'package', 'import', 'true',
                'false', 'nil'}
    tokens = [t for t in tokens if t not in keywords]
    for token in tokens:
        if token in visited_vars:
            continue
        visited_vars.add(token)
        assign_pattern = re.compile(r'(^|;)\s*([a-zA-Z0-9_\[\]]+\s+)?' + re.escape(token) + r'\s*(:=|=)(.*);')
        assign_found = False
        for m in assign_pattern.finditer(func_body):
            line = m.group(0).lstrip('; \n').strip()
            dependencies.append(line)
            right_expr = line.split('=', 1)[1].rstrip(';').strip()
            dependencies += trace_dependencies_go(src_path, func_body, right_expr, visited_vars)
            assign_found = True
        if not assign_found:
            call_pattern = re.compile(re.escape(token) + r'\s*\(')
            if call_pattern.search(func_body):
                sub_body = find_go_function_body(src_path, token)
                if sub_body:
                    dependencies.append(f'func {token}(...) {{...}}')
    return dependencies


# Rust

def find_rs_function_body(src_path, func_name):
    """
    只匹配有函数体的 fn func_name(...) { ... }
    排除trait/声明
    """
    # with open(src_path, "r", encoding="gbk") as f:
    #     code = f.read()
    code = read_file_by_row_encode(src_path)
    code_no_comment = re.sub(r'//.*|/\*[\s\S]*?\*/', '', code)
    pattern = re.compile(r'fn\s+' + re.escape(func_name) + r'\s*\([^)]*\)[^{;]*{', re.MULTILINE)
    matches = list(pattern.finditer(code_no_comment))
    for match in matches:
        func_decl = code_no_comment[match.start(): match.end()]
        if ";" in func_decl:
            continue
        start = match.start()
        stack = 1
        i = match.end()
        while i < len(code_no_comment) and stack > 0:
            if code_no_comment[i] == '{':
                stack += 1
            elif code_no_comment[i] == '}':
                stack -= 1
            i += 1
        return code_no_comment[start:i]
    return None


def trace_dependencies_rs(src_path, func_body, statement, visited_vars=None):
    """
    在Rust文件中找到关键操作的依赖语句链
    """
    if visited_vars is None:
        visited_vars = set()
    dependencies = []
    if re.match(r'^\s*(for|while|if)\s*\(', statement):
        return dependencies
    tokens = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', statement))
    keywords = {'if', 'else', 'return', 'for', 'while', 'loop', 'break', 'continue', 'fn', 'let', 'mut', 'pub',
                'struct', 'enum', 'trait', 'impl', 'match', 'const', 'static', 'ref', 'move', 'super', 'self',
                'Self', 'crate', 'true', 'false', 'as', 'in', 'where', 'use', 'mod', 'type', 'unsafe', 'dyn', 'await'}
    tokens = [t for t in tokens if t not in keywords]
    for token in tokens:
        if token in visited_vars:
            continue
        visited_vars.add(token)
        assign_pattern = re.compile(r'(^|;)\s*(let\s+mut\s+|let\s+)?' + re.escape(token) + r'\s*=([^=].*);')
        assign_found = False
        for m in assign_pattern.finditer(func_body):
            line = m.group(0).lstrip('; \n').strip()
            dependencies.append(line)
            right_expr = line.split('=', 1)[1].rstrip(';').strip()
            dependencies += trace_dependencies_rs(src_path, func_body, right_expr, visited_vars)
            assign_found = True
        if not assign_found:
            call_pattern = re.compile(re.escape(token) + r'\s*\(')
            if call_pattern.search(func_body):
                sub_body = find_rs_function_body(src_path, token)
                if sub_body:
                    dependencies.append(f'fn {token}(...) {{...}}')
    return dependencies


# Vyper

def find_vy_function_body(src_path, func_name):
    # with open(src_path, "r", encoding="gbk") as f:
    #     code = f.read()
    code = read_file_by_row_encode(src_path)
    code_no_comment = re.sub(r'#.*', '', code)
    pattern = re.compile(r'def\s+' + re.escape(func_name) + r'\s*\([^)]*\):', re.MULTILINE)
    matches = list(pattern.finditer(code_no_comment))
    for match in matches:
        lines = code_no_comment[match.end():].splitlines()
        func_lines = []
        indent = None
        for line in lines:
            if not line.strip():
                func_lines.append(line)
                continue
            leading = len(line) - len(line.lstrip())
            if indent is None:
                if leading == 0:
                    break
                indent = leading
            if leading < indent:
                break
            func_lines.append(line)
        return code_no_comment[match.start():match.end()] + '\n' + '\n'.join(func_lines)
    return None


def trace_dependencies_vy(src_path, func_body, statement, visited_vars=None):
    if visited_vars is None:
        visited_vars = set()
    dependencies = []
    if re.match(r'^\s*(for|while|if)\s*\(', statement):
        return dependencies
    tokens = set(re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', statement))
    keywords = {'if', 'else', 'return', 'for', 'while', 'break', 'continue', 'def', 'assert', 'pass', 'True', 'False',
                'None',
                'not', 'and', 'or', 'in', 'is', 'self', 'address', 'uint256', 'int128', 'public', 'private', 'constant',
                'view', 'pure', 'payable', 'event', 'struct'}
    tokens = [t for t in tokens if t not in keywords]
    for token in tokens:
        if token in visited_vars:
            continue
        visited_vars.add(token)
        assign_pattern = re.compile(r'(^|\n)\s*' + re.escape(token) + r'\s*=([^=].*)\n')
        assign_found = False
        for m in assign_pattern.finditer(func_body + '\n'):
            line = m.group(0).lstrip('\n').rstrip('\n').strip()
            dependencies.append(line)
            right_expr = line.split('=', 1)[1].strip()
            dependencies += trace_dependencies_vy(src_path, func_body, right_expr, visited_vars)
            assign_found = True
        if not assign_found:
            call_pattern = re.compile(re.escape(token) + r'\s*\(')
            if call_pattern.search(func_body):
                sub_body = find_vy_function_body(src_path, token)
                if sub_body:
                    dependencies.append(f'def {token}(...) ...')
    return dependencies
