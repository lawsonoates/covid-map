import { Header, Table } from 'semantic-ui-react';

import Searchbar from './searchbar';

function Sidebar(props) {

    return (
        <div>
            <Searchbar onChange={props.onChange} />

            <Header as='h2'>{props.location}</Header>
            <Table>
                <Table.Row>
                    <Table.Cell>Incident Rate</Table.Cell>
                    <Table.Cell textAlign='right'>{props.incidentRate}%</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Case Fatality Ratio</Table.Cell>
                    <Table.Cell textAlign='right'>{props.caseFatalityRatio}%</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Vaccination %</Table.Cell>
                    <Table.Cell textAlign='right'>{props.deaths}</Table.Cell>
                </Table.Row>
            </Table>
            <Table>
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