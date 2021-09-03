import { useState } from 'react';
import { Header, Input } from 'semantic-ui-react';

import axios from 'axios';

import SearchList from './searchList';

function Sidebar(props) {

    const [query, setQuery] = useState('');
    const [results, setResults] = useState({
        regions: []
    });

    function handleChange(e) {
        setQuery(e.target.value)
        fetchRegion(e.target.value)
    }

    const fetchRegion = async query => {

        const config = {
            method: 'post',
            url: 'http://localhost:4000/search',
            responseType: 'json',
            data: { query: query }
        }
        if (query.length !== 0) {
            try {
                const resp = await axios(config)
                setResults({
                    regions: resp.data
                })
            } catch (e) {
                console.log(e);
            }
        } else {
            setResults({
                regions: []
            })
        }
    }

    return (
        <div>
            <Input placeholder='Search...' onChange={handleChange} value={query} />
            <Header as='h2'>{props.region}</Header>
            <p>Total Deaths: {props.deaths}</p>
            <p>Total Cases: {props.confirmed}</p>
            <SearchList results={results}/>
        </div>

    )
}

export default Sidebar;