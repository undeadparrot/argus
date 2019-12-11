<%inherit file="base.mako" />
% for topic in topics:
    <li>
        ${topic.id}
        ${topic.created_date}
    </li>
% endfor

<aside>As of ${now}</aside>

