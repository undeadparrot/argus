<%inherit file="base.mako" />
<%block name="subtitle" >
    <h2>Topics:</h2>
</%block>
% for topic in topics:
    <li>
        ${topic.id}
        ${topic.created_date}
    </li>
% endfor

<aside>As of ${now}</aside>

