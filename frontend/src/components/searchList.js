import { List } from 'semantic-ui-react';

function SearchList(props) {

    return (
        <List>
            {props.results.regions.map((result) => (
                <List.Item key={result.id}>{result.value}</List.Item>
            ))}
        </List>
    );
}

export default SearchList;