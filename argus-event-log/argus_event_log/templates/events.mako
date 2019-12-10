<%inherit file="base.mako" />
<%block name="subtitle" >
<h2>Events:</h2>
</%block>
% if created_event:
<aside class="success">
    <b>Submitted event
        <a href="events/${created_event.uuid}"><small>${created_event.topic.id}-${created_event.uuid}</small></a>!</b>
    <p>
        <pre>${created_event.body}</pre>
    </p>
</aside>
% endif
<form method="post">
    <fieldset>
        <legend>Submit Event:</legend>
        <label for="body">JSON Body:</label>
        <textarea name="body" placeholder="Enter JSON here"></textarea>
        <label for="topic">Topic:</label>
        <select name="topic">
            <option>
                todo
            </option>
        </select>
        <button type="submit">Submit</button>
    </fieldset>
</form>

<br/>

<section>
    <table>
        <thead>
            <tr>
                <td>UUID</td>
                <td>Topic</td>
                <td>Body</td>
                <td>Date</td>
            </tr>
        </thead>

        <tbody>
        % for event in events:
            <tr>
                <td><small>${event.uuid}</small></td>
                <td>${event.topic.id}</td>
                <td><pre>${event.body}</pre></td>
                <td>${event.event_date}</td>
            </tr>
        % endfor
        </tbody>
    </table>
</section>
