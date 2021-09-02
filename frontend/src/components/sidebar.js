import { useState } from 'react';
import { Header } from 'semantic-ui-react';

function Sidebar(props) {

    return (
        <div>
            <Header as='h2'>{props.region}</Header>
            <p>Total Deaths: {props.deaths}</p>
            <p>Total Cases: {props.confirmed}</p>
        </div>

    )
}

export default Sidebar;