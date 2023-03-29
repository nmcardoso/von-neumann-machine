import Head from 'next/head'
import AppNavbar from '@/components/AppNavbar'
import MemoryDumper from '@/components/MemoryDumper'
import { Col, Container, Row } from 'react-bootstrap'
import CodeEditor from '@/components/CodeEditor'
import Console from '@/components/Console'
import RegisterInspector from '@/components/RegisterInspector'

export default function Home() {
  return (
    <>
      <Head>
        <title>Von Neumann Machine</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
        <AppNavbar />
        <Container className="mt-3">
          <Row>
            <Col><CodeEditor /></Col>
            <Col>
              <div>
                <RegisterInspector />
              </div>
              <div>
                <MemoryDumper />
              </div>
            </Col>
          </Row>
          <Row className="mt-3">
            <Col>
              <Console />
            </Col>
          </Row>

        </Container>
      </main>
    </>
  )
}
