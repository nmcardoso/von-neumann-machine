import { Table } from 'react-bootstrap'

export default function RegisterInspector() {
  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Registrador</th>
          <th>Valor</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>PC</td>
          <td>0x0</td>
        </tr>
        <tr>
          <td>Acumulador</td>
          <td>0x0</td>
        </tr>
      </tbody>
    </Table>
  )
}