import axios from 'axios';
import { useState } from 'react/cjs/react.development';
import { Header, Table, Button } from 'semantic-ui-react';

import Searchbar from './searchbar';

function Sidebar(props) {

    const [isRefresh, setIsRefresh] = useState(false);

    // event handler and request to update backend data
    const refresh = async location => {
        setIsRefresh(true)

        const config = {
            method: 'post',
            url: 'http://localhost:4000/db_refresh',
            responseType: 'json'
        }

        try {
            const resp = await axios(config)
            if (resp.data['message'] === 'success') {
                props.fetchStats(props.location)
            } else {
                console.log('server error')
            }

        } catch (e) {
            console.log(e);
        }
        setIsRefresh(false)
    }

    return (
        <div>
            <Searchbar onChange={props.onChange} />

            <Header as='h2'>{props.location}</Header>
            <Table>
                <Table.Row>
                    <Table.Cell>R</Table.Cell>
                    <Table.Cell textAlign='right'>{props.reproductionRate}%</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>7-Day Avg Cases</Table.Cell>
                    <Table.Cell textAlign='right'>{props.newCasesSmoothed}</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Full Vaccination</Table.Cell>
                    <Table.Cell textAlign='right'>{props.peopleFullyVaccinatedPerHundred}%</Table.Cell>
                </Table.Row>
            </Table>
            <Table>
                <Table.Row>
                    <Table.Cell>Total Cases</Table.Cell>
                    <Table.Cell textAlign='right'>{props.totalCases}</Table.Cell>
                </Table.Row>
                <Table.Row>
                    <Table.Cell>Total Deaths</Table.Cell>
                    <Table.Cell textAlign='right'>{props.totalDeaths}</Table.Cell>
                </Table.Row>
            </Table>

            <p>last updated {props.lastUpdateDate}</p>
            <Button loading={isRefresh} onClick={refresh}>Refresh</Button>
        </div>
    )
}

export default Sidebar;