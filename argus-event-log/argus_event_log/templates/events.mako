<%inherit file="base.mako" />
% if created_event:
<aside class="success">
    <b>Submitted event
        <a href="events/${created_event.uuid}"><small>${created_event.topic.id}-${created_event.uuid}</small></a>!</b>
    <p>
        <pre>${created_event.body}</pre>
    </p>
</aside>
% endif
% if events:
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

        <tbody id="event-stream-tbody">
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
% endif

    <script><%text>
        function addEventToTable({uuid, topic, body, date}){
          const rows = [...document.querySelectorAll('#event-stream-tbody tr')];
          while(rows.length > 5){
            const element = rows.pop();
            element.remove();
          }
          const tbody = document.getElementById('event-stream-tbody')
          const tr = document.createElement('tr');
          tr.innerHTML = `
          <td><small>${uuid}</small></td>
          <td>${topic}</td>
          <td><pre>${body}</pre></td>
          <td>${date}</td>
          `;
          tbody.prepend(tr);
        }
        function openEventStream(){
            const ev = new EventSource('events')
            ev.onmessage = function (ev){
             console.info('event', ev.data)
             addEventToTable({uuid: 'blah', topic: ev.type, body: ev.data, date: new Date().toLocaleTimeString()})
            }
        }
    </%text></script>
<button onclick="openEventStream()" style="float:right">Stream Events</button>
<br/>
<form method="post">
    <fieldset>
        <legend>Submit Event:</legend>
        <label for="body">JSON Body:</label>
        <textarea name="body" placeholder="Enter JSON here"></textarea>
        <label for="topic">Topic:</label>
        <select name="topic">
            % for name in ["todo", "notes"]:
            <option>
                ${name}
            </option>
            % endfor
        </select>
        <button type="submit">Submit</button>
    </fieldset>
</form>



