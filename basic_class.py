# 정규식을 위한 re 모듈 불러오기
import re


class Node(object):
    """
    HTML 태그 하나를 가지는 클래스
    내부에 다른 클래스를 가질수도 있음
    가장큰범위는<html></html>
    """
    # 지정한 태그 안의 모든 문자열을 가지고 오기 위한 정규표현식
    _pattern_tag_base = r'<{tag1}.*?>\s*([.\w\W]*?)\s*</{tag1}>'

    # 태그표시 사이의 문자열을 가지고 오기 위한 정규표현식
    pattern_tag_content = r'<[^!].*?>([.\w\W]*)</.*?>'

    # html의 클래스값을 가져오기 위한 정규표현식
    html_class = r'class="(.*?)"'

    # source를 인자로 받아 클래스를 초기화한다.
    def __init__(self, source):
        self.source = source

    # 필요하면 출력하여 오브젝트를 확인할수있다.
    def __str__(self):
        return '{}\n{}'.format(
            super().__str__(),
            self.source
        )

    # 원하는 태그값을 인자로 받아 해당 태그사이의 문자열을 가지고 오는 함수
    # def find_tag(self, tag: object) -> object:
    def find_tag(self, tag):
        """
        주어진 tag 문자열, 또는 문자열리스트 반환
        :param tag: 검색을 원하는 태그 div
        :return: 검색 결과가 1개이상 일경우에는 tag 문자열, 2개이상일 경우에는 tag 문자열
        """
        # 인자 tag의 값을 적용하여 정규표현식을 미리 컴파일한다.
        pattern = re.compile(self._pattern_tag_base.format(tag1 = tag))
        # 위에서 만들어진 정규표현식으로 source를 검색하여 매치되는 문자열을 리스트로 만든다.
        m_list = re.finditer(pattern, self.source)
        # m_list에 값이 있을 경우,
        if m_list:
            # print('m_list', m_list)
            # for item in m_list:
            #     print('item', item)
            # ????
            return_list = [Node(m.group()) for m in m_list]
            # print('return_list', return_list[0])
            # return_list에 값이 있으면 return_list를 반환하고 없으면 return_list의 첫번째값을 반환
            return return_list if len(return_list) > 1 else return_list[0]

    # 태그 사이의 문자열을 반환하는 함수
    @property
    def content(self):
        # 태그 사이에 문자열을 가지고 오기 위한 정규표현식을 미리컴파일
        pattern = re.compile(self.pattern_tag_content)
        # 매치되는 첫번째 문자열를 찾아 m2에
        m2 = re.search(pattern, self.source.strip())
        # m2에 값이 있으면
        if m2:
            # 매치되는 첫번째 그룹요소를 찾아 앞뒤 공백을 제거하고 반환
            return m2.group(1).strip()
        # m2에 값이 없으면 None을 반환
        return None

    @property
    def class_(self):
        """
        해당 Node가 가진 태그의 class 속성의 value를 리턴(문자열)
        :return: 
        """
        # html class 속성값을 가지고오는 정규표현식을 컴파일
        pattern = re.compile(self.html_class)
        # 소스에서 패턴을 찾아 문자열로 반환
        m3 = re.search(pattern, self.source)
        # 값이 있으면
        if m3:
        # 첫번째 그룹 문자열을 반환
            return m3.group(1)
        # 값이 없으면 None을 반환
        return None

# example.html 파일을 열어 데이터를 읽어와 Node 클래스에 대입해 객체화한다.
with open('example.html') as f:
    html = Node(f.read())

# 위에서 만든 클래스 Node 객체 html로 find.tag 함수를 호출한다.(인자는 div)
node_div_list = html.find_tag('div')
# 위 함수에서 생성된 값이 리스트이면,
if type(node_div_list) == list:
    # 리스트를 순회하며
    for node_div in node_div_list:
        # 각 소스에서 html class 속성값을 출력한다.
        print(node_div.class_)
        # 위 값에서 p 태그를 가진 값들의 리스트 생성
        node_p_list = node_div.find_tag('p')
        # 이 값이 리스트이면,
        if type(node_p_list) == list:
            # 리스트를 순회하며
            for node_p in node_p_list:
                # 각 소스에서 html class 속성값과 텍스트 출력
                print('{} / {}'.format(node_p.class_, node_p.content))
        # node_p_list가 리스트가 아니면(결과값이 1개라면)
        else:
            # 반환된 값 출력
            print('{} / {}'.format(node_p.class_, node_p.content))
# node_div_list가 리스트가 아니면(결과값이 1개라면)
else:
    # 반환된 값 출력
    print(node_div_list.class_)

