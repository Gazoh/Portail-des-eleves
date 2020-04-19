import React, { ReactElement } from "react";
import { Poll } from "../../../models/polls";
import { dateFormatter } from "../../../utils/format";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { SelectGroup } from "../../utils/forms/SelectGroup";
import { Form, Formik } from "formik";

type Props = {
    poll: Poll;
};

export function ActivePoll(props: Props) {
    function ChoiceFields() {
        let items: Map<string, ReactElement> = new Map();

        props.poll.choices.forEach(choice => {
            items.set(
                choice.id.toString(),
                <span className="selectgroup-button">{choice.text}</span>
            );
        });

        return (
            <SelectGroup type="vertical" label="" items={items} name="choice" />
        );
    }

    return (
        <Card>
            <Card.Header>
                <Card.Title as="h3">{props.poll.question}</Card.Title>
            </Card.Header>

            <Card.Body>
                <Card.Subtitle className="poll-date">
                    <em>
                        {props.poll.publicationDate &&
                            dateFormatter(props.poll.publicationDate)}
                    </em>
                </Card.Subtitle>

                <Formik
                    initialValues={{
                        shipping: "unregistered",
                        choice: undefined
                    }}
                    onSubmit={(values, { setSubmitting }) => {
                        console.log(values);
                    }}
                >
                    <Form>
                        <ChoiceFields />

                        <div className="text-right ml-auto">
                            <Button variant="outline-success" type="submit">
                                Voter
                            </Button>
                        </div>
                    </Form>
                </Formik>
            </Card.Body>
        </Card>
    );
}
