<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
}
</style>
<?php
    $gitUrl = $_POST['gitUrl'];
    //echo $gitUrl;
    $result =  shell_exec('/usr/bin/python /var/www/html/logic.py ' . $gitUrl);  
    //$result = "1:2:3:4";
    list($count1, $count2, $count3, $count4) = explode(":", $result);
    $html = "<table style='width:100%'><tr><th>Issue</th><th>Count</th></td>";
    $html .= "<tr><td>Total open Issues </td><td>" . $count1 . "</td></tr>"; 
    $html .= "<tr><td>open issues in the last 24 hours </td><td>" . $count2 . "</td></tr>"; 
    $html .= "<tr><td>open issues in the last 24 hours but less than 7 days </td><td>" . $count3 . "</td></tr>"; 
    $html .= "<tr><td>open issues that were opened more than 7 days ago </td><td>" . $count4 . "</td></tr>"; 

    $html .= "</table>";
    echo $html;
?>
