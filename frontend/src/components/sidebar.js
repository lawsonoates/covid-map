import { useState } from 'react';
import { Header, Search, Label } from 'semantic-ui-react';

import axios from 'axios';

const resultRenderer = ({ location }) => <Label content={location} />

function Sidebar(props) {

    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    function handleChange(e) {
        setQuery(e.target.value)
        fetchRegion(e.target.value)
    }

    const fetchRegion = async query => {
        setLoading(true);

        const config = {
            method: 'post',
            url: 'http://localhost:4000/search',
            responseType: 'json',
            data: { query: query }
        }
        if (query.length !== 0) {
            try {
                const resp = await axios(config)
                setResults(resp.data)
            } catch (e) {
                console.log(e);
            }
        } else {
            setResults([])
        }

        setLoading(false);
    }

    return (
        <div>
            <Search
                loading={loading}
                value={query}
                results={results}
                onSearchChange={handleChange}
                resultRenderer={resultRenderer}
                onResultSelect={(e, data) => props.onChange(data.result.location)}
            />

            <Header as='h2'>{props.region}</Header>
            <p>Total Deaths: {props.deaths}</p>
            <p>Total Cases: {props.confirmed}</p>

        </div>

    )
}

export default Sidebar;