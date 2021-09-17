import { Header, Table } from 'semantic-ui-react';

import Searchbar from './searchbar';

function Sidebar(props) {

    return (
        <div>
            <Searchbar onChange={props.onChange} />

            <Header as='h2'>{props.location}</Header>
            <Table>
                {/* <Table.Row>
                    <Table.Cell>Travel Status</Table.Cell>
                    <Table.Cell>{props.status}</Table.Cell>
                </Table.Row> */}
                <Table.Row>
                    <Table.Cell>Total Cases</Table.Cell>
                    <Table.Cell textAlign='right'>{props.confirmed}</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Total Deaths</Table.Cell>
                    <Table.Cell textAlign='right'>{props.deaths}</Table.Cell>
                </Table.Row>
            </Table>

            <p>last updated {props.lastUpdate}</p>
        </div>
    )
}

export default Sidebar;